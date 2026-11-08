/* Indonesia Infrastructure Atlas — application shell and views. */
(function () {
  'use strict';

  const A = window.ATLAS || {};
  const STATUS = A.STATUS || {};
  const STATUS_ORDER = A.STATUS_ORDER || [];
  const SECTORS = A.SECTORS || {};
  const SECTOR_ORDER = A.SECTOR_ORDER || [];
  const STALE_DAYS = A.STALE_DAYS || 183;

  const features = (window.PROJECTS && window.PROJECTS.features) || [];
  const projects = features.map(function (feature) {
    const project = Object.assign({}, feature.properties);
    project.lat = feature.geometry.coordinates[1];
    project.lon = feature.geometry.coordinates[0];
    return project;
  });
  const projectById = new Map(projects.map(function (project) { return [project.id, project]; }));
  const corridors = window.CORRIDORS || [];
  const corridorById = new Map(corridors.map(function (corridor) { return [corridor.id, corridor]; }));
  const stats = window.INFRA_STATS || {};
  const searchIndex = window.INFRA_SEARCH || [];
  const searchProjects = new Map(
    searchIndex.filter(function (entry) { return entry.type === 'project'; })
      .map(function (entry) { return [entry.id, entry]; })
  );
  const searchEstates = new Map(
    searchIndex.filter(function (entry) { return entry.type === 'estate'; })
      .map(function (entry) { return [entry.id, entry]; })
  );

  let estates = window.INFRA_ESTATES || null;
  let estatesState = estates ? 'ready' : 'idle';

  const state = {
    view: 'explore',
    projectId: null,
    corridorId: null,
    q: '',
    sort: 'status',
    filters: {
      sectors: new Set(SECTOR_ORDER),
      statuses: new Set(STATUS_ORDER),
      island: '',
      province: '',
      psn: '',
      corridor: '',
      precision: '',
      freshness: ''
    },
    estateType: 'all',
    estateProvince: '',
    estateSort: 'name',
    expandedEstate: null
  };

  let mapSelectedId = null;
  let initialFitDone = false;
  let lastHash = null;
  let drawerReturnFocus = null;
  let toastTimer = null;
  let sheetDrag = null;
  let sheetSnapIndex = 0;

  const dom = {};
  const mobileQuery = window.matchMedia('(max-width: 860px)');

  /* ---------- helpers ---------- */

  function $(id) { return document.getElementById(id); }

  function esc(value) {
    return String(value == null ? '' : value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function fmtNum(value) {
    const number = Number(value);
    if (!isFinite(number)) return esc(value);
    return new Intl.NumberFormat('en-US', { maximumFractionDigits: 1 }).format(number);
  }

  function fmtCoord(value) {
    const number = Number(value);
    if (!isFinite(number)) return esc(value);
    return new Intl.NumberFormat('en-US', {
      minimumFractionDigits: 4, maximumFractionDigits: 5
    }).format(number);
  }

  function fmtDate(value) {
    if (!value) return '';
    const parsed = new Date(value + 'T00:00:00');
    if (isNaN(parsed.getTime())) return esc(value);
    return new Intl.DateTimeFormat('en-GB', {
      day: 'numeric', month: 'short', year: 'numeric'
    }).format(parsed);
  }

  function daysSince(value) {
    if (!value) return Infinity;
    const parsed = new Date(value + 'T00:00:00');
    if (isNaN(parsed.getTime())) return Infinity;
    return Math.floor((Date.now() - parsed.getTime()) / 86400000);
  }

  function isStale(value) {
    return daysSince(value) > STALE_DAYS;
  }

  function statusLabel(status) {
    return (STATUS[status] && STATUS[status].label) || status || 'Unknown';
  }

  function eventLabel(type) {
    const labels = {
      announced: 'Announced',
      groundbreaking: 'Groundbreaking',
      contract: 'Contract',
      financial_close: 'Financial close',
      section_opened: 'Section opened',
      opened: 'Opened',
      stalled: 'Stalled',
      resumed: 'Resumed',
      target_changed: 'Target changed',
      other: 'Event'
    };
    return labels[type] || String(type || 'Event').replace(/_/g, ' ');
  }

  function sectorLabel(sector, plural) {
    const record = SECTORS[sector];
    if (!record) return sector || '';
    return plural ? record.plural : record.label;
  }

  function statusPill(status) {
    if (!status) return '';
    return '<span class="status-pill s-' + esc(status) + '">' + esc(statusLabel(status)) + '</span>';
  }

  function sectorPill(sector) {
    return '<span class="status-pill plain">' +
      '<svg width="10" height="10" aria-hidden="true"><use href="' +
      esc((SECTORS[sector] && SECTORS[sector].icon) || '#i-place') + '"></use></svg>' +
      esc(sectorLabel(sector)) + '</span>';
  }

  function sectorIcon(sector, size) {
    size = size || 14;
    return '<svg width="' + size + '" height="' + size + '" aria-hidden="true"><use href="' +
      esc((SECTORS[sector] && SECTORS[sector].icon) || '#i-place') + '"></use></svg>';
  }

  function splitProvinces(value) {
    return String(value || '').split(';').map(function (part) { return part.trim(); }).filter(Boolean);
  }

  function provinceShort(project) {
    const list = splitProvinces(project.province);
    if (!list.length) return 'Indonesia';
    return list.length > 1 ? list[0] + ' +' + (list.length - 1) : list[0];
  }

  function toast(message) {
    const el = dom.toast;
    if (!el) return;
    el.textContent = message;
    el.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { el.classList.remove('show'); }, 2600);
  }

  function allSectors() { return new Set(SECTOR_ORDER); }
  function allStatuses() { return new Set(STATUS_ORDER); }

  function hasAdvancedFilters() {
    return !!(state.filters.island || state.filters.province || state.filters.psn ||
      state.filters.corridor || state.filters.precision || state.filters.freshness);
  }

  function hasAnyFilter() {
    return state.filters.sectors.size !== SECTOR_ORDER.length ||
      state.filters.statuses.size !== STATUS_ORDER.length ||
      hasAdvancedFilters();
  }

  function activeFilterCount() {
    let count = 0;
    if (state.filters.sectors.size !== SECTOR_ORDER.length) count += 1;
    if (state.filters.statuses.size !== STATUS_ORDER.length) count += 1;
    ['island', 'province', 'psn', 'corridor', 'precision', 'freshness'].forEach(function (key) {
      if (state.filters[key]) count += 1;
    });
    return count;
  }

  /* ---------- filtering and search ---------- */

  function matchesQuery(project, query) {
    if (!query) return true;
    const entry = searchProjects.get(project.id);
    const haystack = (entry ? entry.text : [
      project.name, project.province, project.island, project.route, project.operator,
      project.subsector, project.corridor_name,
      sectorLabel(project.sector), statusLabel(project.status),
      project.psn === 'yes' ? 'psn' : ''
    ].join(' ')).toLowerCase();
    return query.toLowerCase().split(/\s+/).filter(Boolean).every(function (token) {
      return haystack.indexOf(token) !== -1;
    });
  }

  function passesFilters(project, options) {
    options = options || {};
    if (!options.skipSector && !state.filters.sectors.has(project.sector)) return false;
    if (!options.skipStatus && !state.filters.statuses.has(project.status)) return false;
    if (!options.skipQuery && !matchesQuery(project, state.q)) return false;

    if (state.filters.island && project.island !== state.filters.island) return false;
    if (state.filters.province) {
      const provinces = splitProvinces(project.province);
      if (provinces.indexOf(state.filters.province) === -1) return false;
    }
    if (state.filters.psn && project.psn !== state.filters.psn) return false;
    if (state.filters.corridor && project.corridor_id !== state.filters.corridor) return false;
    if (state.filters.precision && project.precision !== state.filters.precision) return false;
    if (state.filters.freshness === 'fresh' && isStale(project.last_verified)) return false;
    if (state.filters.freshness === 'stale' && !isStale(project.last_verified)) return false;
    return true;
  }

  function filteredProjects() {
    return projects.filter(function (project) { return passesFilters(project); });
  }

  function countByDimension() {
    const bySector = {};
    const byStatus = {};
    projects.forEach(function (project) {
      if (passesFilters(project, { skipSector: true })) {
        bySector[project.sector] = (bySector[project.sector] || 0) + 1;
      }
      if (passesFilters(project, { skipStatus: true })) {
        byStatus[project.status] = (byStatus[project.status] || 0) + 1;
      }
    });
    return { bySector: bySector, byStatus: byStatus };
  }

  function searchScore(project, query) {
    if (!query) return 0;
    const name = project.name.toLowerCase();
    const entry = searchProjects.get(project.id);
    const haystack = (entry ? entry.text : [
      project.name, project.province, project.island, project.route,
      project.operator, project.corridor_name
    ].join(' ')).toLowerCase();
    const normalized = query.toLowerCase().trim();
    if (!normalized) return 0;
    if (name.indexOf(normalized) === 0) return 100;
    if (name.split(/\s+/).some(function (word) { return word.indexOf(normalized) === 0; })) return 70;
    if (name.indexOf(normalized) !== -1) return 50;
    if (haystack.indexOf(normalized) !== -1) return 25;
    return 0;
  }

  function sortProjects(list) {
    const copy = list.slice();
    if (state.q) {
      return copy.sort(function (a, b) {
        return searchScore(b, state.q) - searchScore(a, state.q) ||
          a.name.localeCompare(b.name);
      });
    }
    if (state.sort === 'name') {
      return copy.sort(function (a, b) { return a.name.localeCompare(b.name); });
    }
    if (state.sort === 'verified') {
      return copy.sort(function (a, b) {
        return String(b.last_verified).localeCompare(String(a.last_verified)) ||
          a.name.localeCompare(b.name);
      });
    }
    if (state.sort === 'length') {
      return copy.sort(function (a, b) {
        return (Number(b.length_km) || -1) - (Number(a.length_km) || -1) ||
          a.name.localeCompare(b.name);
      });
    }
    if (state.sort === 'progress') {
      return copy.sort(function (a, b) {
        return (Number(b.progress_pct) || -1) - (Number(a.progress_pct) || -1) ||
          a.name.localeCompare(b.name);
      });
    }
    return copy.sort(function (a, b) {
      const ai = STATUS_ORDER.indexOf(a.status);
      const bi = STATUS_ORDER.indexOf(b.status);
      return (ai < 0 ? 99 : ai) - (bi < 0 ? 99 : bi) || a.name.localeCompare(b.name);
    });
  }

  function openShare(project) {
    const length = Number(project.length_km);
    const open = Number(project.operational_km);
    if (!length || !isFinite(length) || !isFinite(open) || open <= 0) return null;
    return Math.max(0, Math.min(100, (open / length) * 100));
  }

  /* ---------- routing ---------- */

  function resetFilters() {
    state.filters.sectors = allSectors();
    state.filters.statuses = allStatuses();
    state.filters.island = '';
    state.filters.province = '';
    state.filters.psn = '';
    state.filters.corridor = '';
    state.filters.precision = '';
    state.filters.freshness = '';
  }

  function parseHash() {
    let raw = location.hash || '#/explore';
    if (raw.charAt(0) === '#' && raw.charAt(1) !== '/') {
      const legacyId = raw.slice(1);
      if (projectById.has(legacyId)) {
        state.view = 'project';
        state.projectId = legacyId;
        resetFilters();
        return;
      }
      raw = '#/explore';
    }

    const withoutHash = raw.slice(2);
    const split = withoutHash.split('?');
    const parts = split[0].split('/').filter(Boolean);
    const params = new URLSearchParams(split[1] || '');
    const view = parts[0] || 'explore';

    resetFilters();
    state.q = params.get('q') || '';
    state.sort = params.get('sort') || 'status';
    state.projectId = null;
    state.corridorId = null;
    state.estateType = params.get('type') || 'all';
    state.estateProvince = params.get('eprovince') || '';
    state.estateSort = params.get('esort') || 'name';

    const sector = params.get('sector');
    if (sector !== null) {
      state.filters.sectors = new Set(sector.split(',').filter(function (key) {
        return SECTOR_ORDER.indexOf(key) !== -1;
      }));
    }
    const status = params.get('status');
    if (status !== null) {
      state.filters.statuses = new Set(status.split(',').filter(function (key) {
        return STATUS_ORDER.indexOf(key) !== -1;
      }));
    }
    state.filters.island = params.get('island') || '';
    state.filters.province = params.get('province') || '';
    state.filters.psn = params.get('psn') || '';
    state.filters.corridor = params.get('corridor') || '';
    state.filters.precision = params.get('precision') || '';
    state.filters.freshness = params.get('fresh') || '';

    if (view === 'project') {
      state.view = 'project';
      state.projectId = parts[1] || null;
      if (!projectById.has(state.projectId)) {
        state.view = 'explore';
        state.projectId = null;
      }
    } else if (view === 'corridors') {
      state.view = 'corridors';
      state.corridorId = parts[1] || null;
      if (state.corridorId && !corridorById.has(state.corridorId)) state.corridorId = null;
    } else if (view === 'estates') {
      state.view = 'estates';
    } else if (view === 'data') {
      state.view = 'data';
    } else {
      state.view = 'explore';
    }
  }

  function buildHash() {
    let base = '#/' + (state.view === 'project' ? 'explore' : state.view);
    if (state.view === 'project' && state.projectId) {
      base = '#/project/' + state.projectId;
    } else if (state.view === 'corridors' && state.corridorId) {
      base = '#/corridors/' + state.corridorId;
    }
    const params = new URLSearchParams();
    if (state.filters.sectors.size !== SECTOR_ORDER.length) {
      params.set('sector', Array.from(state.filters.sectors).join(','));
    }
    if (state.filters.statuses.size !== STATUS_ORDER.length) {
      params.set('status', Array.from(state.filters.statuses).join(','));
    }
    if (state.filters.island) params.set('island', state.filters.island);
    if (state.filters.province) params.set('province', state.filters.province);
    if (state.filters.psn) params.set('psn', state.filters.psn);
    if (state.filters.corridor) params.set('corridor', state.filters.corridor);
    if (state.filters.precision) params.set('precision', state.filters.precision);
    if (state.filters.freshness) params.set('fresh', state.filters.freshness);
    if (state.q) params.set('q', state.q);
    if (state.sort !== 'status') params.set('sort', state.sort);
    if (state.view === 'estates') {
      if (state.estateType !== 'all') params.set('type', state.estateType);
      if (state.estateProvince) params.set('eprovince', state.estateProvince);
      if (state.estateSort !== 'name') params.set('esort', state.estateSort);
    }
    const query = params.toString();
    return base + (query ? '?' + query : '');
  }

  function setHash(hash, push) {
    lastHash = hash;
    if (location.hash === hash) return;
    try {
      if (push) history.pushState(null, '', hash);
      else history.replaceState(null, '', hash);
    } catch (error) {
      location.hash = hash;
    }
  }

  function commit(push) {
    renderAll();
    setHash(buildHash(), !!push);
    if (state.view === 'estates') ensureEstates();
  }

  function applyRoute() {
    parseHash();
    renderAll();
    if (state.view === 'estates') ensureEstates();
    requestAnimationFrame(function () { window.AtlasMap && window.AtlasMap.resize(); });
    if (!initialFitDone && !state.projectId) {
      initialFitDone = true;
      requestAnimationFrame(function () {
        if (window.AtlasMap) {
          window.AtlasMap.fitAll(mobileQuery.matches ? dom.rail.offsetHeight + 16 : 8);
        }
      });
    }
  }

  /* ---------- header, tabs, chips ---------- */

  function renderHeader() {
    const totalProjects = (stats.projects && stats.projects.total) || projects.length;
    const totalCorridors = (stats.corridors && stats.corridors.total) || corridors.length;
    const totalEstates = (stats.estates && stats.estates.total) || (estates ? estates.length : 178);
    dom.statProjects.textContent = fmtNum(totalProjects);
    dom.statCorridors.textContent = fmtNum(totalCorridors);
    dom.statEstates.textContent = fmtNum(totalEstates);
    if (dom.search.value !== state.q) dom.search.value = state.q;
    dom.tabCountExplore.textContent = fmtNum(totalProjects);
  }

  function renderTabs() {
    const active = state.view === 'project' ? 'explore' : state.view;
    dom.tabs.forEach(function (tab) {
      tab.setAttribute('aria-selected', String(tab.getAttribute('data-view') === active));
    });
  }

  function renderSectorChips() {
    const counts = countByDimension().bySector;
    const allSelected = state.filters.sectors.size === SECTOR_ORDER.length;
    let html = '<button class="chip" data-sector-all aria-pressed="' + allSelected + '">' +
      'All<span class="chip-count">' + fmtNum(projects.filter(function (project) {
        return passesFilters(project, { skipSector: true });
      }).length) + '</span></button>';
    SECTOR_ORDER.forEach(function (sector) {
      const count = counts[sector] || 0;
      const pressed = state.filters.sectors.has(sector);
      const short = (SECTORS[sector] && SECTORS[sector].short) || sectorLabel(sector, true);
      html += '<button class="chip' + (count === 0 ? ' is-zero' : '') + '" data-sector="' +
        esc(sector) + '" aria-pressed="' + pressed + '" aria-label="' +
        esc(sectorLabel(sector, true)) + '">' +
        esc(short) + '<span class="chip-count">' + fmtNum(count) + '</span></button>';
    });
    dom.sectorChips.innerHTML = html;
  }

  function renderStatusChips() {
    const counts = countByDimension().byStatus;
    let html = '';
    STATUS_ORDER.forEach(function (status) {
      const count = counts[status] || 0;
      const pressed = state.filters.statuses.has(status);
      const short = (STATUS[status] && STATUS[status].short) || statusLabel(status);
      html += '<button class="chip' + (count === 0 ? ' is-zero' : '') + '" data-status="' +
        esc(status) + '" aria-pressed="' + pressed + '" aria-label="' +
        esc(statusLabel(status)) + '"><span class="dot" style="--c:' +
        esc((STATUS[status] && STATUS[status].color) || '#667085') + '"></span>' +
        esc(short) + '<span class="chip-count">' + fmtNum(count) + '</span></button>';
    });
    dom.statusChips.innerHTML = html;
  }

  function renderActiveFilters() {
    const chips = [];
    if (state.filters.sectors.size !== SECTOR_ORDER.length) {
      Array.from(state.filters.sectors).forEach(function (sector) {
        chips.push({ key: 'sector:' + sector, label: sectorLabel(sector, true) });
      });
    }
    if (state.filters.statuses.size !== STATUS_ORDER.length) {
      Array.from(state.filters.statuses).forEach(function (status) {
        chips.push({ key: 'status:' + status, label: statusLabel(status) });
      });
    }
    if (state.filters.island) chips.push({ key: 'island', label: state.filters.island });
    if (state.filters.province) chips.push({ key: 'province', label: state.filters.province });
    if (state.filters.psn) chips.push({ key: 'psn', label: 'PSN: ' + state.filters.psn });
    if (state.filters.corridor) {
      const corridor = corridorById.get(state.filters.corridor);
      chips.push({ key: 'corridor', label: corridor ? corridor.name : state.filters.corridor });
    }
    if (state.filters.precision) chips.push({ key: 'precision', label: 'Precision: ' + state.filters.precision });
    if (state.filters.freshness) chips.push({ key: 'freshness', label: state.filters.freshness === 'fresh' ? 'Verified < 6 months' : 'Stale' });

    if (!chips.length) {
      dom.activeFilters.hidden = true;
      dom.activeFilters.innerHTML = '';
    } else {
      dom.activeFilters.hidden = false;
      dom.activeFilters.innerHTML = chips.map(function (chip) {
        return '<span class="active-filter">' + esc(chip.label) +
          '<button type="button" data-remove="' + esc(chip.key) + '" aria-label="Remove filter ' +
          esc(chip.label) + '">&times;</button></span>';
      }).join('');
    }

    const count = activeFilterCount();
    dom.filterBadge.hidden = count === 0;
    dom.filterBadge.textContent = String(count);
    dom.clearFilters.hidden = !hasAnyFilter();
    dom.popoverSummary.textContent = filteredProjects().length + ' of ' + projects.length + ' projects match';
  }

  function renderFilterControls() {
    if (!dom.filterGrid) return;
    const islandOptions = ['<option value="">Any island</option>'].concat(
      ((stats.projects && stats.projects.island) ? Object.keys(stats.projects.island) : [])
        .sort().map(function (island) {
          return '<option value="' + esc(island) + '">' + esc(island) + '</option>';
        })
    ).join('');
    const provinceOptions = ['<option value="">Any province</option>'].concat(
      ((stats.projects && stats.projects.by_province) ? Object.keys(stats.projects.by_province) : [])
        .sort().map(function (province) {
          return '<option value="' + esc(province) + '">' + esc(province) + '</option>';
        })
    ).join('');
    const corridorOptions = ['<option value="">Any corridor</option>'].concat(
      corridors.map(function (corridor) {
        return '<option value="' + esc(corridor.id) + '">' + esc(corridor.name) + '</option>';
      })
    ).join('');

    dom.filterGrid.innerHTML =
      '<div class="field"><label for="f-island">Island</label><select id="f-island" data-filter="island">' + islandOptions + '</select></div>' +
      '<div class="field"><label for="f-province">Province</label><select id="f-province" data-filter="province">' + provinceOptions + '</select></div>' +
      '<div class="field"><label for="f-psn">PSN status</label><select id="f-psn" data-filter="psn"><option value="">Any</option><option value="yes">PSN</option><option value="no">Not PSN</option><option value="unknown">Unknown</option></select></div>' +
      '<div class="field"><label for="f-corridor">Corridor</label><select id="f-corridor" data-filter="corridor">' + corridorOptions + '</select></div>' +
      '<div class="field"><label for="f-precision">Precision</label><select id="f-precision" data-filter="precision"><option value="">Any</option><option value="exact">Exact</option><option value="approximate">Approximate</option><option value="regency">Regency</option><option value="province">Province</option></select></div>' +
      '<div class="field"><label for="f-fresh">Verification</label><select id="f-fresh" data-filter="freshness"><option value="">Any date</option><option value="fresh">Under 6 months</option><option value="stale">Stale</option></select></div>';

    syncFilterControls();
  }

  function syncFilterControls() {
    if (!dom.filterGrid) return;
    const map = {
      island: state.filters.island,
      province: state.filters.province,
      psn: state.filters.psn,
      corridor: state.filters.corridor,
      precision: state.filters.precision,
      freshness: state.filters.freshness
    };
    Object.keys(map).forEach(function (key) {
      const field = dom.filterGrid.querySelector('[data-filter="' + key + '"]');
      if (field) field.value = map[key];
    });
  }

  /* ---------- project list ---------- */

  function rowFigure(project) {
    const bits = [];
    if (project.length_km) bits.push(fmtNum(project.length_km) + ' km');
    if (project.operational_km) bits.push(fmtNum(project.operational_km) + ' km open');
    if (!bits.length && project.investment_idr_t) bits.push('Rp ' + fmtNum(project.investment_idr_t) + ' T');
    if (!bits.length && project.capacity) bits.push(fmtNum(project.capacity) + ' ' + project.capacity_unit);
    if (!bits.length && project.opened_year) bits.push('Opened ' + project.opened_year);
    if (!bits.length && project.expected_open_year) bits.push('Target ' + project.expected_open_year);
    return bits.join(' · ') || 'No figure yet';
  }

  function renderProjectRows(list) {
    if (!list.length) {
      dom.projectList.innerHTML = '<li><div class="list-empty">' +
        '<svg aria-hidden="true"><use href="#i-search"></use></svg>' +
        '<h3>No projects match</h3>' +
        '<p>Try removing a filter or searching for a province, corridor or project name.</p>' +
        '<button class="filter-button" id="empty-clear" type="button">Clear all filters</button>' +
        '</div></li>';
      const clear = $('empty-clear');
      if (clear) clear.addEventListener('click', function () { resetFilters(); state.q = ''; commit(false); });
      return;
    }

    dom.projectList.innerHTML = list.map(function (project) {
      const share = project.progress_pct ? Number(project.progress_pct) : openShare(project);
      const shareLabel = project.progress_pct ? fmtNum(project.progress_pct) + '% built' :
        (share !== null ? fmtNum(share) + '% open' : '');
      const current = state.projectId === project.id ? 'true' : 'false';
      const psn = project.psn === 'yes' ? ' · PSN' : '';
      const sub = provinceShort(project) + ' · ' + sectorLabel(project.sector) + psn;
      return '<li><button type="button" class="project-row" data-project="' + esc(project.id) +
        '" aria-current="' + current + '" aria-label="' + esc(project.name + ', ' +
        statusLabel(project.status) + ', ' + provinceShort(project)) + '">' +
        '<span class="row-status" style="--c:' + esc((STATUS[project.status] && STATUS[project.status].color) || '#667085') + '"></span>' +
        '<span class="row-icon">' + sectorIcon(project.sector, 13) + '</span>' +
        '<span class="row-main">' +
        '<span class="row-line"><span class="row-title">' + esc(project.name) + '</span>' +
        statusPill(project.status) + '</span>' +
        '<span class="row-sub">' + esc(sub) + '</span>' +
        '<span class="row-figure"><span>' + esc(rowFigure(project)) + '</span>' +
        (shareLabel ? '<span class="row-progress"><span style="width:' + Math.max(2, Math.min(100, share)) +
          '%;--c:' + esc((STATUS[project.status] && STATUS[project.status].color) || '#667085') + '"></span></span>' +
          '<span>' + esc(shareLabel) + '</span>' : '') +
        '</span></span>' +
        '<span class="row-chevron" aria-hidden="true">›</span>' +
        '</button></li>';
    }).join('');
  }

  function renderExplore() {
    dom.exploreContent.hidden = false;
    dom.viewPanel.hidden = true;
    dom.exploreContent.style.display = 'flex';

    const list = sortProjects(filteredProjects());
    const total = projects.length;

    renderSectorChips();
    renderStatusChips();
    renderActiveFilters();
    syncFilterControls();

    dom.resultCount.innerHTML = list.length === total
      ? '<strong>' + fmtNum(total) + '</strong> projects'
      : '<strong>' + fmtNum(list.length) + '</strong> of ' + fmtNum(total) + ' projects';
    dom.footCount.textContent = fmtNum(list.length);
    dom.footTotal.textContent = fmtNum(total);
    dom.mapCount.textContent = fmtNum(list.length);
    dom.sort.value = state.sort;

    renderProjectRows(list);
    const selectedRow = dom.projectList.querySelector('[aria-current="true"]');
    if (selectedRow && state.projectId) {
      selectedRow.scrollIntoView({ block: 'nearest' });
    }
  }

  /* ---------- drawer ---------- */

  function drawerWidth() {
    return mobileQuery.matches ? 0 : 420;
  }

  function openDrawer() {
    const wasHidden = dom.drawer.hidden;
    if (wasHidden) {
      drawerReturnFocus = document.activeElement;
      dom.drawer.hidden = false;
      requestAnimationFrame(function () { dom.drawer.classList.add('open'); });
    }
    dom.drawer.setAttribute('aria-hidden', 'false');
    // The drawer is modal. Make the map behind it inert so its overlapping
    // approximate markers are not competing focus targets. The project list
    // stays available as the accessible equivalent and the drawer has
    // previous/next controls.
    if (dom.mapWrap) dom.mapWrap.inert = true;
    if (wasHidden) {
      setTimeout(function () { dom.drawerClose.focus(); }, 40);
    }
  }

  function closeDrawer() {
    if (dom.drawer.hidden) return;
    dom.drawer.classList.remove('open');
    dom.drawer.setAttribute('aria-hidden', 'true');
    if (dom.mapWrap) dom.mapWrap.inert = false;
    setTimeout(function () {
      if (!dom.drawer.classList.contains('open')) dom.drawer.hidden = true;
    }, 260);
    if (drawerReturnFocus && typeof drawerReturnFocus.focus === 'function') {
      drawerReturnFocus.focus();
    }
    drawerReturnFocus = null;
  }

  function metricCard(label, value) {
    return '<div class="metric"><div class="k">' + esc(label) + '</div><div class="v">' + value + '</div></div>';
  }

  function projectMetrics(project) {
    const metrics = [];
    if (project.length_km) metrics.push(metricCard('Corridor length', fmtNum(project.length_km) + ' <small>km</small>'));
    if (project.operational_km) metrics.push(metricCard('Open', fmtNum(project.operational_km) + ' <small>km</small>'));
    if (project.construction_km) metrics.push(metricCard('Under construction', fmtNum(project.construction_km) + ' <small>km</small>'));
    if (project.investment_idr_t) metrics.push(metricCard('Investment', 'Rp ' + fmtNum(project.investment_idr_t) + ' <small>T</small>'));
    if (project.capacity) metrics.push(metricCard('Capacity', fmtNum(project.capacity) + ' <small>' + esc(project.capacity_unit) + '</small>'));
    if (project.opened_year) metrics.push(metricCard('Opened', esc(project.opened_year)));
    if (metrics.length < 2) metrics.push(metricCard('PSN', esc(project.psn === 'yes' ? 'Yes' : project.psn === 'no' ? 'No' : 'Unknown')));
    if (metrics.length < 2) metrics.push(metricCard('Last verified', esc(fmtDate(project.last_verified))));
    return metrics.slice(0, 4).join('');
  }

  function projectSourceList(project) {
    const sources = project.sources || [];
    if (!sources.length) {
      return '<p class="basis">No source is attached to this row yet.</p>';
    }
    return '<ul class="source-list">' + sources.map(function (source) {
      const claim = source.claim ? ' · ' + esc(source.claim) : '';
      const published = source.published_on ? ' · published ' + esc(fmtDate(source.published_on)) : '';
      return '<li><div class="src-head"><span class="src-name">' + esc(source.title || source.publisher) +
        '</span><span class="src-type">' + esc(source.source_type || 'source') + '</span></div>' +
        '<div class="src-meta">' + esc(source.publisher) + claim + ' · retrieved ' +
        esc(fmtDate(source.retrieved_on)) + published + '</div>' +
        (source.url ? '<a href="' + esc(source.url) + '" target="_blank" rel="noopener">Open source ↗</a>' : '') +
        '</li>';
    }).join('') + '</ul>';
  }

  function renderProjectDrawer(project) {
    dom.drawerPills.innerHTML = statusPill(project.status) + sectorPill(project.sector);
    dom.drawerTitle.textContent = project.name;
    dom.drawerLoc.textContent = project.province + ' · ' + project.route;

    const basisSource = (project.sources && project.sources[0]) || null;
    const share = project.progress_pct ? Number(project.progress_pct) : openShare(project);
    const shareLabel = project.progress_pct ? 'Reported construction progress' : 'Operational share';

    let body = '';
    body += '<div class="metric-grid">' + projectMetrics(project) + '</div>';

    if (share !== null && isFinite(share)) {
      body += '<div class="progress-block"><div class="progress-head"><span>' + esc(shareLabel) +
        '</span><strong>' + fmtNum(share) + '%</strong></div><div class="progress-track">' +
        '<span style="width:' + Math.max(0, Math.min(100, share)) + '%;--c:' +
        esc((STATUS[project.status] && STATUS[project.status].color) || '#c2410c') + '"></span></div></div>';
    }

    body += '<section class="detail-section"><h3>Why this status</h3>' +
      '<p class="basis">' + esc(project.status_basis) + '</p>' +
      '<div class="basis-meta">Status as of ' + esc(fmtDate(project.status_as_of || project.last_verified)) +
      (basisSource ? ' · ' + esc(basisSource.publisher) : '') + '</div></section>';

    body += '<section class="detail-section"><h3>Evidence</h3><ul class="evidence-list">' +
      '<li><time>' + esc(fmtDate(project.last_verified)) + '</time><span>Record verified' +
      (basisSource ? ' against ' + esc(basisSource.title) : '') + '.</span></li>' +
      (project.opened_year ? '<li><time>' + esc(project.opened_year) + '</time><span>Opened to service.</span></li>' : '') +
      (project.corridor_name ? '<li><time>Corridor</time><span>Part of ' + esc(project.corridor_name) +
        '. <a class="related-link" href="#/corridors/' + esc(project.corridor_id) + '">Open corridor ↗</a></span></li>' : '') +
      '</ul></section>';

    if (project.events && project.events.length) {
      body += '<section class="detail-section"><h3>Timeline</h3>' +
        '<ul class="evidence-list event-list">' + project.events.map(function (event) {
          return '<li><time>' + esc(fmtDate(event.event_date)) + '</time><span><b>' +
            esc(eventLabel(event.event_type)) + '</b> · ' + esc(event.description) +
            (event.source_url ? ' <a href="' + esc(event.source_url) + '" target="_blank" rel="noopener">Source ↗</a>' : '') +
            '</span></li>';
        }).join('') + '</ul></section>';
    }

    body += '<section class="detail-section"><h3>Sources</h3>' + projectSourceList(project) + '</section>';

    if (project.notes) {
      body += '<section class="detail-section"><h3>Notes and conflicts</h3>' +
        '<p class="notes-callout">' + esc(project.notes) + '</p></section>';
    }

    body += '<section class="detail-section"><h3>Data quality</h3><ul class="evidence-list">' +
      '<li><time>Coordinates</time><span>' + esc(project.precision) + ' precision · ' +
      fmtCoord(project.lat) + ', ' + fmtCoord(project.lon) + '</span></li>' +
      '<li><time>PSN</time><span>' + esc(project.psn === 'yes' ? 'National Strategic Project' :
        project.psn === 'no' ? 'Not a PSN' : 'PSN status unknown') + '</span></li>' +
      '<li><time>Verification</time><span>' + esc(project.verification) +
      ' · status as of ' + esc(fmtDate(project.status_as_of)) + '</span></li>' +
      '<li><time>Record</time><span>' + esc(project.id) + '</span></li>' +
      '</ul></section>';

    dom.drawerBody.innerHTML = body;
    dom.drawerBody.scrollTop = 0;

    const list = sortProjects(filteredProjects());
    const index = list.findIndex(function (item) { return item.id === project.id; });
    const prev = index > 0 ? list[index - 1] : null;
    const next = index !== -1 && index < list.length - 1 ? list[index + 1] : null;

    dom.drawerFoot.innerHTML =
      '<div class="drawer-meta"><span>' + esc(project.precision) + ' coordinates</span>' +
      '<span>Verified ' + esc(fmtDate(project.last_verified)) + '</span>' +
      '<span>' + esc(project.id) + '</span></div>' +
      '<div class="drawer-nav">' +
      '<button class="nav-btn" type="button" data-nav="prev"' + (prev ? '' : ' disabled') + '>' +
      '<svg aria-hidden="true"><use href="#i-chevron-left"></use></svg>' + (prev ? esc(prev.name) : 'Previous') + '</button>' +
      '<button class="share-btn" type="button" data-share="' + esc(project.id) + '">' +
      '<svg width="11" height="11" aria-hidden="true"><use href="#i-share"></use></svg> Share</button>' +
      '<button class="nav-btn" type="button" data-nav="next"' + (next ? '' : ' disabled') + '>' +
      (next ? esc(next.name) : 'Next') + '<svg aria-hidden="true"><use href="#i-chevron-right"></use></svg></button>' +
      '</div>';

    dom.drawer.dataset.kind = 'project';
    dom.drawer.dataset.id = project.id;
    openDrawer();
  }

  function corridorSegmentTable(corridor) {
    const segments = corridor.segments || [];
    if (!segments.length) {
      return '<p class="basis">No section list has been published for this corridor. The route total is the only verified figure; no progress share is inferred.</p>';
    }
    return '<div class="segment-wrap"><table class="segment-table"><thead><tr>' +
      '<th scope="col">Section</th><th scope="col">Length</th><th scope="col">Status</th><th scope="col">Opened</th>' +
      '</tr></thead><tbody>' + segments.map(function (segment) {
        const color = (STATUS[segment.status] && STATUS[segment.status].color) || '#667085';
        const note = segment.notes ? '<span class="segment-note">' + esc(segment.notes) + '</span>' : '';
        const opened = segment.opened_year ? esc(segment.opened_year) :
          (segment.expected_open_year ? 'by ' + esc(segment.expected_open_year) : '—');
        return '<tr><th scope="row">' + esc(segment.name) + note + '</th>' +
          '<td class="num">' + fmtNum(segment.length_km) + ' km</td>' +
          '<td><span class="status-dot" style="--c:' + esc(color) + '"></span>' + esc(statusLabel(segment.status)) + '</td>' +
          '<td class="num">' + opened + '</td></tr>';
      }).join('') + '</tbody></table></div>';
  }

  function corridorTimeline(corridor) {
    const events = corridor.events || [];
    if (!events.length) {
      return '<p class="basis">No dated event is recorded for this corridor yet. Openings are tracked at project level where an exact date is available.</p>';
    }
    const groups = [];
    events.forEach(function (event) {
      const year = String(event.event_date || '').slice(0, 4) || 'Undated';
      let group = groups[groups.length - 1];
      if (!group || group.year !== year) {
        group = { year: year, items: [] };
        groups.push(group);
      }
      group.items.push(event);
    });
    return '<ol class="timeline">' + groups.map(function (group) {
      return '<li class="timeline-year"><div class="timeline-year-label">' + esc(group.year) + '</div>' +
        '<ul>' + group.items.map(function (event) {
          return '<li><div class="timeline-date">' + esc(fmtDate(event.event_date)) + '</div>' +
            '<div class="timeline-body"><b>' + esc(eventLabel(event.event_type)) + '</b> · ' +
            esc(event.project_name) + '. ' + esc(event.description) +
            (event.source_url ? ' <a href="' + esc(event.source_url) + '" target="_blank" rel="noopener">Source ↗</a>' : '') +
            '</div></li>';
        }).join('') + '</ul></li>';
    }).join('') + '</ol>';
  }

  function renderCorridorDrawer(corridor) {
    dom.drawerPills.innerHTML = '<span class="status-pill plain">Trans corridor</span>' +
      '<span class="status-pill plain">' + esc(corridor.island) + '</span>';
    dom.drawerTitle.textContent = corridor.name;
    dom.drawerLoc.textContent = corridor.definition;

    const parts = corridorParts(corridor);
    const word = corridorWord(corridor);
    const metricTitle = word === 'connected' ? 'Connected' : word === 'paved' ? 'Paved' : 'Operating';
    const share = parts.hasTotal && parts.operational ? (parts.operational / parts.total) * 100 : null;
    const remaining = parts.hasTotal && (parts.operational || parts.construction)
      ? Math.max(parts.total - parts.operational - parts.construction, 0)
      : null;
    const segments = corridor.segments || [];
    const segmentKm = Number(corridor.segment_km) || 0;
    const state = corridorState(corridor);

    let body = '<div class="metric-grid">';
    body += metricCard('Total', parts.hasTotal ? fmtNum(parts.total) + ' <small>km</small>' : 'Not defined');
    body += metricCard(metricTitle, parts.operational ? fmtNum(parts.operational) + ' <small>km</small>' : '—');
    body += metricCard('Under construction', parts.construction ? fmtNum(parts.construction) + ' <small>km</small>' : '—');
    body += metricCard('Not yet open', remaining ? fmtNum(remaining) + ' <small>km</small>' : '—');
    body += '</div>';

    if (parts.hasTotal && hasBreakdown(parts)) {
      body += corridorBar(corridor) + corridorLegend(corridor);
    }

    if (share !== null) {
      body += '<div class="progress-block"><div class="progress-head"><span>' + esc(corridor.metric) +
        '</span><strong>' + fmtNum(share) + '%</strong></div><div class="progress-track">' +
        '<span style="width:' + pctOf(parts.operational, parts.total) +
        '%;--c:var(--operating)"></span></div></div>';
    }

    body += '<section class="detail-section"><h3>Definition and scope</h3><p class="basis">' +
      esc(corridor.definition) + '</p><div class="basis-meta">Metric: ' + esc(corridor.metric) +
      (corridor.as_of ? ' · as of ' + esc(fmtDate(corridor.as_of)) : '') + '</div></section>';

    body += '<section class="detail-section"><h3>Series coverage</h3><p class="basis">' +
      (segments.length
        ? segments.length + ' sections covering ' + fmtNum(segmentKm) + ' km' +
          (parts.hasTotal ? ', ' + fmtNum(corridor.segment_share) + '% of the route total' : '') + '. ' +
          (state.key === 'partial'
            ? 'The section table is partial: the unlisted length stays in the corridor total rather than being assigned to a section.'
            : 'The section lengths reconcile to the published corridor total.')
        : 'No segment table. The route total is published, but no operational-km series exists, so no percentage is estimated.') +
      '</p><div class="basis-meta"><span class="corridor-state ' + esc(state.key) + '">' +
      esc(state.label) + '</span></div></section>';

    if (corridor.notes) {
      body += '<section class="detail-section"><h3>Notes and conflicts</h3><p class="notes-callout">' +
        esc(corridor.notes) + '</p></section>';
    }

    body += '<section class="detail-section"><h3>Segments</h3>' + corridorSegmentTable(corridor) + '</section>';
    body += '<section class="detail-section"><h3>Timeline</h3>' + corridorTimeline(corridor) + '</section>';

    body += '<section class="detail-section"><h3>Source</h3><ul class="source-list"><li>' +
      '<div class="src-head"><span class="src-name">' + esc(corridor.source_title || corridor.source_publisher) +
      '</span><span class="src-type">' + esc(corridor.source_type || 'source') + '</span></div>' +
      '<div class="src-meta">' + esc(corridor.source_publisher) + ' · retrieved ' +
      esc(fmtDate(corridor.retrieved_on)) + '</div>' +
      (corridor.source_url ? '<a href="' + esc(corridor.source_url) + '" target="_blank" rel="noopener">Open source ↗</a>' : '') +
      '</li></ul></section>';

    dom.drawerBody.innerHTML = body;
    dom.drawerBody.scrollTop = 0;

    const index = corridors.findIndex(function (item) { return item.id === corridor.id; });
    dom.drawerFoot.innerHTML =
      '<div class="drawer-meta"><span>Metric: ' + esc(corridor.metric) + '</span>' +
      (corridor.as_of ? '<span>As of ' + esc(fmtDate(corridor.as_of)) + '</span>' : '') +
      '<span>' + esc(corridor.id) + '</span></div>' +
      '<div class="drawer-nav">' +
      '<button class="nav-btn" type="button" data-corridor-nav="prev"' + (index > 0 ? '' : ' disabled') + '>' +
      '<svg aria-hidden="true"><use href="#i-chevron-left"></use></svg>Previous</button>' +
      '<button class="share-btn" type="button" data-share="' + esc(corridor.id) + '">' +
      '<svg width="11" height="11" aria-hidden="true"><use href="#i-share"></use></svg> Share</button>' +
      '<button class="nav-btn" type="button" data-corridor-nav="next"' +
      (index !== -1 && index < corridors.length - 1 ? '' : ' disabled') + '>Next' +
      '<svg aria-hidden="true"><use href="#i-chevron-right"></use></svg></button>' +
      '</div>';

    dom.drawer.dataset.kind = 'corridor';
    dom.drawer.dataset.id = corridor.id;
    openDrawer();
  }

  function renderDrawer() {
    if (state.projectId && projectById.has(state.projectId)) {
      renderProjectDrawer(projectById.get(state.projectId));
      return;
    }
    if (state.view === 'corridors' && state.corridorId && corridorById.has(state.corridorId)) {
      renderCorridorDrawer(corridorById.get(state.corridorId));
      return;
    }
    closeDrawer();
  }

  /* ---------- map sync ---------- */

  function renderMap() {
    if (!window.AtlasMap) return;
    const list = filteredProjects();
    window.AtlasMap.setProjects(list);
    dom.mapCount.textContent = fmtNum(list.length);

    if (state.projectId && projectById.has(state.projectId) &&
        list.some(function (project) { return project.id === state.projectId; })) {
      if (mapSelectedId !== state.projectId) {
        window.AtlasMap.select(state.projectId, { drawerWidth: drawerWidth() });
        mapSelectedId = state.projectId;
      }
    } else if (mapSelectedId) {
      window.AtlasMap.clearSelection();
      mapSelectedId = null;
    }
  }

  /* ---------- corridors view ---------- */

  function corridorWord(corridor) {
    const metric = String(corridor.metric || '').toLowerCase();
    if (metric.indexOf('connected') !== -1) return 'connected';
    if (metric.indexOf('paved') !== -1) return 'paved';
    return 'operational';
  }

  function corridorParts(corridor) {
    const total = Number(corridor.total_km) || 0;
    const operational = Number(corridor.operational_km) || 0;
    const construction = Number(corridor.construction_km) || 0;
    const planned = Number(corridor.planned_km) || 0;
    const gap = total ? Math.max(total - operational - construction - planned, 0) : 0;
    return {
      total: total,
      operational: operational,
      construction: construction,
      planned: planned,
      gap: gap,
      hasTotal: total > 0
    };
  }

  function pctOf(value, total) {
    if (!total) return 0;
    return Math.max(0, Math.min(100, (value / total) * 100));
  }

  function corridorBar(corridor) {
    const parts = corridorParts(corridor);
    if (!parts.hasTotal) return '';
    let bar = '';
    if (parts.operational) bar += '<span class="op" style="width:' + pctOf(parts.operational, parts.total) + '%"></span>';
    if (parts.construction) bar += '<span class="uc" style="width:' + pctOf(parts.construction, parts.total) + '%"></span>';
    if (parts.planned) bar += '<span class="planned" style="width:' + pctOf(parts.planned, parts.total) + '%"></span>';
    if (parts.gap) bar += '<span class="gap" style="width:' + pctOf(parts.gap, parts.total) + '%"></span>';
    return '<div class="corridor-bar" role="img" aria-label="' + esc(corridor.name) + ' status shares">' + bar + '</div>';
  }

  function corridorLegend(corridor) {
    const parts = corridorParts(corridor);
    const gapLabel = corridorWord(corridor) === 'connected' ? 'Not connected' : 'Unallocated';
    const items = [];
    if (parts.operational) items.push('<span><i class="sw op"></i>Operating ' + fmtNum(parts.operational) + ' km</span>');
    if (parts.construction) items.push('<span><i class="sw uc"></i>Construction ' + fmtNum(parts.construction) + ' km</span>');
    if (parts.planned) items.push('<span><i class="sw planned"></i>Planned ' + fmtNum(parts.planned) + ' km</span>');
    if (parts.gap) items.push('<span><i class="sw gap"></i>' + gapLabel + ' ' + fmtNum(parts.gap) + ' km</span>');
    return items.length ? '<div class="corridor-legend">' + items.join('') + '</div>' : '';
  }

  function hasBreakdown(parts) {
    return Boolean(parts.operational || parts.construction || parts.planned);
  }

  function corridorState(corridor) {
    const parts = corridorParts(corridor);
    if (!parts.hasTotal) return { key: 'none', label: 'No series' };
    if (!parts.operational) return { key: 'total', label: 'Route total only' };
    const share = Number(corridor.segment_share);
    if (corridor.segment_share !== null && corridor.segment_share !== undefined && isFinite(share) && share < 99.5) {
      return { key: 'partial', label: 'Partial segment table' };
    }
    return { key: 'full', label: 'Complete series' };
  }

  function corridorCard(corridor) {
    const parts = corridorParts(corridor);
    const word = corridorWord(corridor);
    const state = corridorState(corridor);
    const share = parts.hasTotal && parts.operational ? (parts.operational / parts.total) * 100 : null;
    const segments = corridor.segments || [];
    const segmentKm = Number(corridor.segment_km) || 0;

    let figure;
    if (parts.hasTotal && parts.operational) {
      figure = '<strong>' + fmtNum(parts.operational) + '</strong> of ' + fmtNum(parts.total) + ' km ' + word;
    } else if (parts.hasTotal) {
      figure = '<strong>' + fmtNum(parts.total) + ' km</strong> route · no progress series';
    } else {
      figure = '<strong>No series</strong> · aggregate withheld';
    }

    let meta = '';
    if (share !== null) meta = fmtNum(share) + '% ' + word;
    else if (parts.hasTotal) meta = 'Route total only';
    if (corridor.as_of) meta += (meta ? ' · ' : '') + 'as of ' + fmtDate(corridor.as_of);

    const coverage = segments.length
      ? segments.length + ' sections · ' + fmtNum(segmentKm) + ' km' +
        (parts.hasTotal && segmentKm ? ' (' + fmtNum(corridor.segment_share) + '% of route)' : '')
      : 'No segment table';

    return '<button type="button" class="corridor-card" data-corridor="' + esc(corridor.id) + '">' +
      '<div class="corridor-head"><h3>' + esc(corridor.name) + '</h3>' +
      '<span class="corridor-metric">' + esc(corridor.metric) + '</span></div>' +
      '<div class="corridor-figure">' + figure + '</div>' +
      (meta ? '<div class="corridor-meta">' + esc(meta) + '</div>' : '') +
      '<p class="corridor-def">' + esc(corridor.definition) + '</p>' +
      (hasBreakdown(parts) ? corridorBar(corridor) + corridorLegend(corridor) : '') +
      '<div class="corridor-foot"><span class="corridor-state ' + esc(state.key) + '">' + esc(state.label) + '</span>' +
      '<span>' + esc(coverage) + '</span></div>' +
      (corridor.notes ? '<div class="corridor-gap">' + esc(corridor.notes) + '</div>' : '') +
      '</button>';
  }

  function renderCorridors() {
    dom.exploreContent.hidden = true;
    dom.exploreContent.style.display = 'none';
    dom.viewPanel.hidden = false;
    dom.viewPanel.innerHTML =
      '<div class="corridor-intro"><h2>Trans corridors</h2>' +
      '<p>Five defined corridors. Network progress is shown where a published kilometre breakdown exists; where it does not, the route total is published without a guessed percentage. Segment coverage and unallocated length stay visible.</p></div>' +
      '<div class="corridor-list">' + corridors.map(corridorCard).join('') + '</div>';
  }

  /* ---------- estates view ---------- */

  function ensureEstates() {
    if (estatesState === 'ready' || estatesState === 'loading') return;
    estatesState = 'loading';
    const script = document.createElement('script');
    script.src = 'data/estates.js';
    script.onload = function () {
      estates = window.INFRA_ESTATES || [];
      estatesState = 'ready';
      if (state.view === 'estates') renderAll();
    };
    script.onerror = function () {
      estatesState = 'error';
      if (state.view === 'estates') renderAll();
    };
    document.body.appendChild(script);
  }

  function estateTypeLabel(type) {
    return type === 'sez' ? 'SEZ' : type === 'both' ? 'SEZ + estate' : 'Industrial estate';
  }

  function filteredEstates() {
    if (!estates) return [];
    const query = state.q.toLowerCase().trim();
    return estates.filter(function (estate) {
      if (state.estateType !== 'all') {
        if (state.estateType === 'both' && estate.type !== 'both') return false;
        if (state.estateType === 'sez' && estate.type !== 'sez' && estate.type !== 'both') return false;
        if (state.estateType === 'industrial_estate' && estate.type !== 'industrial_estate' && estate.type !== 'both') return false;
      }
      if (state.estateProvince && estate.province !== state.estateProvince) return false;
      if (query) {
        const entry = searchEstates.get(estate.id);
        const haystack = (entry ? entry.text :
          [estate.name, estate.province, estate.regency, estate.developer, estate.sector_focus]
            .join(' ')).toLowerCase();
        if (!query.split(/\s+/).every(function (token) { return haystack.indexOf(token) !== -1; })) return false;
      }
      return true;
    }).sort(function (a, b) {
      if (state.estateSort === 'area') return (Number(b.area_ha) || 0) - (Number(a.area_ha) || 0);
      if (state.estateSort === 'province') {
        return a.province.localeCompare(b.province) || a.name.localeCompare(b.name);
      }
      return a.name.localeCompare(b.name);
    });
  }

  function estateRow(estate) {
    const expanded = state.expandedEstate === estate.id;
    const source = estate.source_publisher || 'Source';
    const coords = fmtCoord(estate.lat) + ', ' + fmtCoord(estate.lon);
    return '<div class="estate-row"><button type="button" data-estate="' + esc(estate.id) +
      '" aria-expanded="' + expanded + '"><span><span class="estate-name">' + esc(estate.name) +
      '<span class="type-tag">' + esc(estateTypeLabel(estate.type)) + '</span></span>' +
      '<span class="estate-sub">' + esc(estate.regency) + ' · ' + esc(estate.province) + '</span></span>' +
      '<span class="estate-area">' + fmtNum(estate.area_ha) + ' ha<small>' + esc(estate.status) +
      '</small></span></button>' +
      (expanded ? '<div class="estate-detail">' +
        '<dl><dt>Developer</dt><dd>' + esc(estate.developer) + '</dd>' +
        '<dt>Sector focus</dt><dd>' + esc(estate.sector_focus || 'Not stated') + '</dd>' +
        '<dt>Legal basis</dt><dd>' + esc(estate.legal_basis || 'Not stated') + '</dd>' +
        '<dt>Established</dt><dd>' + esc(estate.established_year || 'Not stated') + '</dd>' +
        '<dt>Website</dt><dd>' + (estate.website ? '<a href="' + esc(estate.website) + '" target="_blank" rel="noopener">' + esc(estate.website) + '</a>' : 'Not recorded') + '</dd>' +
        '<dt>Coordinates</dt><dd>' + esc(coords) + ' · ' + esc(estate.precision) + '</dd>' +
        '<dt>Source</dt><dd>' + esc(source) + (estate.source_url ? ' · <a href="' + esc(estate.source_url) + '" target="_blank" rel="noopener">open ↗</a>' : '') + '</dd>' +
        '<dt>Verified</dt><dd>' + esc(fmtDate(estate.last_verified)) + '</dd></dl>' +
        (estate.notes ? '<p class="estate-detail-note">' + esc(estate.notes) + '</p>' : '') +
        '</div>' : '') + '</div>';
  }

  function renderEstates() {
    dom.exploreContent.hidden = true;
    dom.exploreContent.style.display = 'none';
    dom.viewPanel.hidden = false;

    if (estatesState === 'loading') {
      dom.viewPanel.innerHTML = '<div class="data-view"><h2>Estates and SEZs</h2>' +
        '<p class="lede">Loading the estate table…</p></div>';
      return;
    }
    if (estatesState === 'error') {
      dom.viewPanel.innerHTML = '<div class="data-view"><h2>Estates and SEZs</h2>' +
        '<p class="notes-callout">The estate payload could not be loaded. Rebuild the site data and try again.</p></div>';
      return;
    }
    if (!estates) {
      dom.viewPanel.innerHTML = '<div class="data-view"><h2>Estates and SEZs</h2>' +
        '<p class="lede">Loading the estate table…</p></div>';
      ensureEstates();
      return;
    }

    const list = filteredEstates();
    const typeCounts = { all: estates.length, sez: 0, industrial_estate: 0, both: 0 };
    estates.forEach(function (estate) {
      if (estate.type === 'sez' || estate.type === 'both') typeCounts.sez += 1;
      if (estate.type === 'industrial_estate' || estate.type === 'both') typeCounts.industrial_estate += 1;
      if (estate.type === 'both') typeCounts.both += 1;
    });
    const provinces = Array.from(new Set(estates.map(function (estate) { return estate.province; }))).sort();
    const totalArea = estates.reduce(function (sum, estate) { return sum + (Number(estate.area_ha) || 0); }, 0);
    const types = [
      { key: 'all', label: 'All', count: typeCounts.all },
      { key: 'sez', label: 'SEZ', count: typeCounts.sez },
      { key: 'industrial_estate', label: 'Industrial', count: typeCounts.industrial_estate },
      { key: 'both', label: 'Both', count: typeCounts.both }
    ];

    dom.viewPanel.innerHTML =
      '<div class="estate-tools"><h2>Estates and SEZs</h2>' +
      '<p>' + fmtNum(estates.length) + ' records: ' + fmtNum(typeCounts.sez) + ' SEZs and ' +
      fmtNum(typeCounts.industrial_estate) + ' industrial-estate designations, including ' +
      fmtNum(typeCounts.both) + ' zones shared with SEZs. This is a table view; the map layer waits for verified coordinates.</p>' +
      '<div class="estate-summary">' +
      '<div><div class="k">Zones</div><div class="v">' + fmtNum(estates.length) + '</div></div>' +
      '<div><div class="k">Total area</div><div class="v">' + fmtNum(Math.round(totalArea)) + ' <small>ha</small></div></div>' +
      '<div><div class="k">SEZs</div><div class="v">' + fmtNum(typeCounts.sez) + '</div></div>' +
      '<div><div class="k">Provinces</div><div class="v">' + fmtNum(provinces.length) + '</div></div>' +
      '</div>' +
      '<div class="chip-row" style="margin-bottom:9px">' + types.map(function (type) {
        return '<button class="chip" data-estate-type="' + esc(type.key) + '" aria-pressed="' +
          (state.estateType === type.key) + '">' + esc(type.label) +
          '<span class="chip-count">' + fmtNum(type.count) + '</span></button>';
      }).join('') + '</div>' +
      '<div class="filter-actions" style="margin-top:0">' +
      '<label class="field" style="flex:1"><span class="sr-only">Province</span><select id="estate-province">' +
      '<option value="">Any province</option>' + provinces.map(function (province) {
        return '<option value="' + esc(province) + '"' + (state.estateProvince === province ? ' selected' : '') +
          '>' + esc(province) + '</option>';
      }).join('') + '</select></label>' +
      '<label class="field" style="flex:1"><span class="sr-only">Sort estates</span><select id="estate-sort">' +
      '<option value="name"' + (state.estateSort === 'name' ? ' selected' : '') + '>Name A–Z</option>' +
      '<option value="area"' + (state.estateSort === 'area' ? ' selected' : '') + '>Largest area</option>' +
      '<option value="province"' + (state.estateSort === 'province' ? ' selected' : '') + '>Province</option>' +
      '</select></label></div>' +
      '<div class="corridor-meta" style="margin-top:9px">' + fmtNum(list.length) + ' of ' +
      fmtNum(estates.length) + ' zones shown</div></div>' +
      '<div class="estate-list">' + (list.length ? list.map(estateRow).join('') :
        '<div class="list-empty"><h3>No estates match</h3><p>Try another province or type.</p></div>') + '</div>' +
      '<p class="estate-note">Coordinates: 25 SEZs use official KEK points, 20 large industrial estates use OSM/Nominatim points, and the rest are regency centroids. The 19-name 2025 gap is documented in the Data view rather than guessed. Sources: Kemenperin-derived estate list, KEK profiles and <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap (ODbL)</a>.</p>';

    const chips = dom.viewPanel.querySelectorAll('[data-estate-type]');
    chips.forEach(function (chip) {
      chip.addEventListener('click', function () {
        state.estateType = chip.getAttribute('data-estate-type');
        commit(false);
      });
    });
    const provinceSelect = $('estate-province');
    if (provinceSelect) provinceSelect.addEventListener('change', function () {
      state.estateProvince = provinceSelect.value;
      commit(false);
    });
    const sortSelect = $('estate-sort');
    if (sortSelect) sortSelect.addEventListener('change', function () {
      state.estateSort = sortSelect.value;
      commit(false);
    });
  }

  /* ---------- data view ---------- */

  function coverageRows() {
    const rows = (stats.coverage || []).map(function (row) {
      return '<tr><td class="layer">' + esc(row.label) + '<br><span style="color:var(--muted);font-size:9px">' +
        esc(row.universe) + '</span></td>' +
        '<td class="num">' + fmtNum(row.current) + '</td>' +
        '<td class="num">' + fmtNum(row.target) + '</td>' +
        '<td class="num ' + (row.status === 'met' ? 'ok' : 'gap') + '">' +
        (row.status === 'met' ? 'Met' : (row.gap ? '+' + fmtNum(row.gap) : '—')) + '</td></tr>';
    }).join('');
    return '<table class="coverage-table"><thead><tr><th>Layer</th><th>Now</th><th>Target</th><th>Gap</th></tr></thead><tbody>' +
      rows + '</tbody></table>';
  }

  function sourceRegister() {
    const sources = stats.sources || [];
    if (!sources.length) return '<p>Source register is not available in this build.</p>';
    return '<ul class="source-register">' + sources.map(function (source) {
      return '<li><div class="src-title">' + esc(source.title) + '</div>' +
        '<div class="src-meta">' + esc(source.publisher) + ' · ' + esc(source.source_type) +
        ' · retrieved ' + esc(fmtDate(source.retrieved_on)) + '</div></li>';
    }).join('') + '</ul>';
  }

  function downloadList() {
    const downloads = stats.downloads || [];
    return '<div class="download-list">' + downloads.map(function (item) {
      return '<a class="download" href="' + esc(item.file) + '" download>' +
        '<span>' + esc(item.label) + ' <small>' + esc(item.meta) + '</small></span>' +
        '<svg width="13" height="13" aria-hidden="true"><use href="#i-download"></use></svg></a>';
    }).join('') + '</div>';
  }

  function renderData() {
    dom.exploreContent.hidden = true;
    dom.exploreContent.style.display = 'none';
    dom.viewPanel.hidden = false;

    const projectStats = stats.projects || {};
    const estateStats = stats.estates || {};
    const sectorCounts = projectStats.by_sector || {};
    const transportCount = (sectorCounts.railway || 0) + (sectorCounts.airport || 0) +
      (sectorCounts.seaport || 0);
    const roadCount = sectorCounts.road || 0;
    const generated = stats.generated_on ? fmtDate(stats.generated_on) : fmtDate(new Date().toISOString().slice(0, 10));

    dom.viewPanel.innerHTML =
      '<div class="data-view">' +
      '<h2>Data and methods</h2>' +
      '<p class="lede">What this atlas covers, how a status is decided, where the numbers come from, and what is still missing. Counts are generated from the curated tables at build time.</p>' +

      '<section class="data-section"><h3>Coverage</h3>' + coverageRows() +
      '<p style="margin-top:7px;color:var(--muted);font-size:9px">Generated ' + esc(generated) +
      ' · data as of ' + esc(fmtDate(stats.data_as_of)) + '</p></section>' +

      '<section class="data-section"><h3>What this is</h3>' +
      '<p>A curated, source-linked map of major Indonesian infrastructure. It is not a live tracker, an official government dataset, or a complete list.</p>' +
      '<p>Every row needs a source and a verification date. A status change needs an official source or two independent sources. Conflicts stay visible in the notes.</p></section>' +

      '<section class="data-section"><h3>Status definitions</h3><ul class="def-list">' +
      STATUS_ORDER.map(function (status) {
        const meaning = {
          planned: 'Designated, contracted or tendered; no physical construction.',
          under_construction: 'Any material construction active, even if another section is already open.',
          operating: 'Fully open before the two-year window; context for the network.',
          recently_completed: 'Fully open on or after 6 November 2024.',
          stalled: 'Officially delayed or reported stalled.'
        }[status] || '';
        return '<li><b>' + esc(statusLabel(status)) + '</b><span>' + esc(meaning) + '</span></li>';
      }).join('') + '</ul></section>' +

      '<section class="data-section"><h3>Inclusion rules</h3>' +
      '<p><b>Roads:</b> major toll corridors and PSN national roads. <b>Airports and seaports:</b> PSN or KPBU designated. <b>Factories:</b> PSN manufacturing plants or private plants with investment of at least Rp 1 trillion; estates and pure mining pits are excluded. <b>Estates:</b> the Kemenperin industrial-estate list and official SEZ profiles, one row per zone.</p>' +
      '<p>The Bali, Malacca and Sunda strait bridges are excluded by scope. Estates remain table-only until their coordinates are verified.</p></section>' +

      '<section class="data-section"><h3>Known gaps</h3><ul class="gap-list">' +
      '<li>' + fmtNum(projectStats.total || 0) + ' projects: ' + fmtNum(projectStats.with_investment || 0) +
      ' with an investment figure, ' + fmtNum(projectStats.with_progress || 0) +
      ' with reported progress and ' + fmtNum(projectStats.with_length || 0) + ' with a route length.</li>' +
      '<li>Transport PSN: ' + fmtNum(transportCount) + ' of 35 represented (' +
      fmtNum(sectorCounts.railway || 0) + ' rail, ' + fmtNum(sectorCounts.airport || 0) +
      ' airports, ' + fmtNum(sectorCounts.seaport || 0) +
      ' seaports). Status is as of 19 February 2026, the date of the Kemenhub review.</li>' +
      '<li>Factories and smelters: ' + fmtNum(sectorCounts.factory || 0) +
      ' plants mapped. Plant points are approximate; capacity and investment are only as good as the cited company or press source. Transport points are also approximate, and the PSN review gives no rail length or asset capacity.</li>' +
      '<li>Estate coverage: ' + fmtNum(estateStats.industrial || 0) +
      ' industrial-estate designations and ' + fmtNum(estateStats.sez || 0) +
      ' SEZs (' + fmtNum(estateStats.total || 0) + ' rows, ' + fmtNum(estateStats.both || 0) +
      ' shared) against a 2026 benchmark of 179 industrial estates. The ' +
      fmtNum(estateStats.gap_rows || 0) + '-name gap ledger is in Downloads: nine named 2025 additions and ten unidentified names.</li>' +
      '<li>Estate coordinates: ' + fmtNum((estateStats.coordinate_sources || {}).official || 0) +
      ' SEZ/shared zones use official KEK points, ' +
      fmtNum((estateStats.coordinate_sources || {}).osm || 0) +
      ' large industrial estates use OSM/Nominatim points, and ' +
      fmtNum((estateStats.coordinate_sources || {}).regency || 0) +
      ' still use regency centroids.</li>' +
      '<li>Trans Sulawesi and Trans Kalimantan publish a route total only: no current operational-km series or segment table was found. Trans Sumatra and Trans Papua segment tables are partial and say so.</li>' +
      '<li>' + fmtNum((projectStats.psn && projectStats.psn.unknown) || 0) + ' of ' +
      fmtNum(roadCount) + ' road rows have unknown PSN status; ' +
      fmtNum(projectStats.precision && projectStats.precision.approximate || 0) + ' of ' +
      fmtNum(projectStats.total || 0) + ' rows use approximate coordinates.</li>' +
      '<li>Verification: ' + fmtNum((projectStats.verification && projectStats.verification.official) || 0) +
      ' official, ' + fmtNum((projectStats.verification && projectStats.verification.single) || 0) +
      ' single-source, ' + fmtNum((projectStats.verification && projectStats.verification.dual) || 0) +
      ' dual-source.</li>' +
      '</ul></section>' +

      '<section class="data-section"><h3>Source register</h3>' + sourceRegister() + '</section>' +

      '<section class="data-section"><h3>Downloads</h3>' + downloadList() + '</section>' +

      '<section class="data-section"><h3>Changelog</h3><ul class="changelog">' +
      '<li><time>8 Nov 2026</time><span>Five Trans corridors, 44 dated segments and six project events. Trans Java joins as the fifth corridor; roads reach the 45-corridor target with three planned Trans Sumatra concessions.</span></li>' +
      '<li><time>8 Nov 2026</time><span>Added 27 factories and smelters: 19 operating, 3 recently completed, 4 under construction and 1 stalled, with operators, capacity, investment and source claims.</span></li>' +
      '<li><time>8 Nov 2026</time><span>Added 15 PSN toll corridors from BPJT; roads now 42 of the 45 target corridors.</span></li>' +
      '<li><time>8 Nov 2026</time><span>Estate reconciliation: a 19-name gap ledger and OSM/Nominatim coordinates for 20 of the 40 largest industrial estates.</span></li>' +
      '<li><time>7 Nov 2026</time><span>Added the 35 transport PSN projects: 13 railways, 7 airports and 15 seaports, with status and investment claims from the Kemenhub review.</span></li>' +
      '<li><time>7 Nov 2026</time><span>New shell: four views, search, filters, map v2 and this data page.</span></li>' +
      '<li><time>6 Nov 2026</time><span>178 estates and SEZs gathered; 25 official SEZ profiles and the Kemenperin-derived list.</span></li>' +
      '<li><time>6 Nov 2026</time><span>27 toll-road corridors, four Trans corridor summaries and the v2 data foundation.</span></li>' +
      '</ul></section>' +
      '</div>';
  }

  /* ---------- render orchestration ---------- */

  function renderAll() {
    renderHeader();
    renderTabs();

    if (state.view === 'explore' || state.view === 'project') {
      renderExplore();
    } else if (state.view === 'corridors') {
      renderCorridors();
    } else if (state.view === 'estates') {
      renderEstates();
    } else if (state.view === 'data') {
      renderData();
    }

    renderDrawer();
    renderMap();
  }

  /* ---------- mobile sheet ---------- */

  function sheetSnaps() {
    const viewport = window.innerHeight - (mobileQuery.matches ? 56 : 64);
    return [220, Math.round(viewport * 0.52), viewport - 12];
  }

  function setSheetHeight(height, animate) {
    if (!mobileQuery.matches) {
      dom.rail.style.height = '';
      document.documentElement.style.removeProperty('--sheet-h');
      return;
    }
    const snaps = sheetSnaps();
    const bounded = Math.max(snaps[0], Math.min(snaps[2], height));
    let nearestIndex = 0;
    snaps.forEach(function (snap, index) {
      if (Math.abs(snap - bounded) < Math.abs(snaps[nearestIndex] - bounded)) nearestIndex = index;
    });
    sheetSnapIndex = nearestIndex;
    if (animate === false) dom.rail.classList.add('is-dragging');
    else dom.rail.classList.remove('is-dragging');
    dom.rail.classList.toggle('is-peek', bounded <= 240);
    dom.rail.style.height = bounded + 'px';
    document.documentElement.style.setProperty('--sheet-h', bounded + 'px');
    if (window.AtlasMap) window.AtlasMap.resize();
  }

  function initSheet() {
    if (!mobileQuery.matches) {
      setSheetHeight(0);
      return;
    }
    const snaps = sheetSnaps();
    setSheetHeight(snaps[0]);
  }

  function bindSheet() {
    if (!dom.sheetHandle) return;

    dom.sheetHandle.addEventListener('pointerdown', function (event) {
      if (!mobileQuery.matches) return;
      const startHeight = dom.rail.getBoundingClientRect().height;
      sheetDrag = { startY: event.clientY, startHeight: startHeight };
      dom.rail.classList.add('is-dragging');
      dom.sheetHandle.setPointerCapture(event.pointerId);
      event.preventDefault();
    });

    dom.sheetHandle.addEventListener('pointermove', function (event) {
      if (!sheetDrag) return;
      const height = sheetDrag.startHeight + (sheetDrag.startY - event.clientY);
      setSheetHeight(height, false);
    });

    dom.sheetHandle.addEventListener('pointerup', function (event) {
      if (!sheetDrag) return;
      sheetDrag = null;
      dom.rail.classList.remove('is-dragging');
      const current = dom.rail.getBoundingClientRect().height;
      const snaps = sheetSnaps();
      const nearest = snaps.reduce(function (best, snap) {
        return Math.abs(snap - current) < Math.abs(best - current) ? snap : best;
      }, snaps[0]);
      setSheetHeight(nearest);
      dom.sheetHandle.releasePointerCapture(event.pointerId);
    });

    dom.sheetHandle.addEventListener('keydown', function (event) {
      if (!mobileQuery.matches) return;
      const snaps = sheetSnaps();
      const current = dom.rail.getBoundingClientRect().height;
      let index = 0;
      snaps.forEach(function (snap, i) {
        if (Math.abs(snap - current) < Math.abs(snaps[index] - current)) index = i;
      });
      if (event.key === 'ArrowUp') {
        setSheetHeight(snaps[Math.min(snaps.length - 1, index + 1)]);
        event.preventDefault();
      } else if (event.key === 'ArrowDown') {
        setSheetHeight(snaps[Math.max(0, index - 1)]);
        event.preventDefault();
      }
    });

    window.addEventListener('resize', function () {
      if (mobileQuery.matches) {
        const snaps = sheetSnaps();
        setSheetHeight(snaps[Math.min(sheetSnapIndex, snaps.length - 1)]);
      } else {
        setSheetHeight(0);
      }
    });
  }

  /* ---------- navigation and events ---------- */

  function selectProject(id, push) {
    if (!projectById.has(id)) return;
    state.projectId = id;
    state.view = 'project';
    commit(push !== false);
    const row = dom.projectList.querySelector('[data-project="' + id + '"]');
    if (row) row.scrollIntoView({ block: 'nearest' });
  }

  function closeProject() {
    if (state.view !== 'project') return;
    state.view = 'explore';
    state.projectId = null;
    commit(false);
  }

  function selectCorridor(id, push) {
    if (!corridorById.has(id)) return;
    state.view = 'corridors';
    state.corridorId = id;
    commit(push !== false);
  }

  function closeCorridor() {
    if (state.view !== 'corridors') return;
    state.view = 'corridors';
    state.corridorId = null;
    commit(false);
  }

  function shareLink(id) {
    const url = location.href.split('#')[0] + buildHash();
    function fallback() {
      const area = document.createElement('textarea');
      area.value = url;
      area.setAttribute('readonly', '');
      area.style.position = 'fixed';
      area.style.opacity = '0';
      document.body.appendChild(area);
      area.select();
      let ok = false;
      try { ok = document.execCommand('copy'); } catch (error) { ok = false; }
      document.body.removeChild(area);
      toast(ok ? 'Link copied' : 'Copy the address bar to share this view');
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(url).then(function () { toast('Link copied'); }).catch(fallback);
    } else {
      fallback();
    }
  }

  function bindEvents() {
    dom.tabs.forEach(function (tab) {
      tab.addEventListener('click', function () {
        const view = tab.getAttribute('data-view');
        state.view = view;
        state.projectId = null;
        state.corridorId = null;
        if (mobileQuery.matches) {
          const snaps = sheetSnaps();
          setSheetHeight(view === 'data' ? snaps[2] : snaps[1]);
        }
        commit(true);
      });
    });

    dom.search.addEventListener('input', function () {
      state.q = dom.search.value;
      if (state.view === 'data' || state.view === 'corridors') {
        state.view = 'explore';
        state.projectId = null;
        state.corridorId = null;
      }
      commit(false);
    });

    document.addEventListener('keydown', function (event) {
      if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'k') {
        event.preventDefault();
        dom.search.focus();
        dom.search.select();
      }
    });

    dom.search.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') {
        if (state.q) {
          state.q = '';
          dom.search.value = '';
          commit(false);
        } else {
          dom.search.blur();
        }
      }
    });

    dom.sectorChips.addEventListener('click', function (event) {
      const all = event.target.closest('[data-sector-all]');
      if (all) {
        state.filters.sectors = allSectors();
        commit(false);
        return;
      }
      const chip = event.target.closest('[data-sector]');
      if (!chip) return;
      const sector = chip.getAttribute('data-sector');
      if (state.filters.sectors.size === SECTOR_ORDER.length) {
        state.filters.sectors = new Set([sector]);
      } else if (state.filters.sectors.has(sector)) {
        state.filters.sectors.delete(sector);
      } else {
        state.filters.sectors.add(sector);
      }
      commit(false);
    });

    dom.statusChips.addEventListener('click', function (event) {
      const chip = event.target.closest('[data-status]');
      if (!chip) return;
      const status = chip.getAttribute('data-status');
      if (state.filters.statuses.has(status)) state.filters.statuses.delete(status);
      else state.filters.statuses.add(status);
      commit(false);
    });

    dom.activeFilters.addEventListener('click', function (event) {
      const button = event.target.closest('[data-remove]');
      if (!button) return;
      const value = button.getAttribute('data-remove');
      const split = value.split(':');
      if (split[0] === 'sector') {
        state.filters.sectors.delete(split[1]);
      } else if (split[0] === 'status') {
        state.filters.statuses.delete(split[1]);
      } else if (split[0] === 'freshness') {
        state.filters.freshness = '';
      } else {
        state.filters[split[0]] = '';
      }
      commit(false);
    });

    dom.clearFilters.addEventListener('click', function () {
      resetFilters();
      commit(false);
    });

    dom.moreFilters.addEventListener('click', function () {
      const open = dom.filterPopover.hidden;
      dom.filterPopover.hidden = !open;
      dom.moreFilters.setAttribute('aria-expanded', String(open));
      if (open) syncFilterControls();
    });

    dom.popoverClose.addEventListener('click', function () {
      dom.filterPopover.hidden = true;
      dom.moreFilters.setAttribute('aria-expanded', 'false');
    });

    document.addEventListener('click', function (event) {
      if (dom.filterPopover.hidden) return;
      if (dom.filterPopover.contains(event.target) || dom.moreFilters.contains(event.target)) return;
      dom.filterPopover.hidden = true;
      dom.moreFilters.setAttribute('aria-expanded', 'false');
    });

    dom.filterGrid.addEventListener('change', function (event) {
      const field = event.target.closest('[data-filter]');
      if (!field) return;
      state.filters[field.getAttribute('data-filter')] = field.value;
      commit(false);
    });

    dom.sort.addEventListener('change', function () {
      state.sort = dom.sort.value;
      commit(false);
    });

    dom.projectList.addEventListener('click', function (event) {
      const row = event.target.closest('[data-project]');
      if (!row) return;
      selectProject(row.getAttribute('data-project'), true);
    });

    dom.projectList.addEventListener('keydown', function (event) {
      if (event.key !== 'ArrowDown' && event.key !== 'ArrowUp') return;
      const rows = Array.from(dom.projectList.querySelectorAll('[data-project]'));
      const index = rows.indexOf(document.activeElement);
      if (index === -1) return;
      event.preventDefault();
      const next = event.key === 'ArrowDown' ? Math.min(rows.length - 1, index + 1) : Math.max(0, index - 1);
      rows[next].focus();
    });

    dom.drawerClose.addEventListener('click', function () {
      if (state.projectId) closeProject();
      else closeCorridor();
    });

    dom.drawer.addEventListener('click', function (event) {
      const corridorLink = event.target.closest('[href^="#/corridors/"]');
      if (corridorLink) {
        event.preventDefault();
        selectCorridor(corridorLink.getAttribute('href').replace('#/corridors/', ''), true);
        return;
      }
      const share = event.target.closest('[data-share]');
      if (share) {
        shareLink(share.getAttribute('data-share'));
        return;
      }
      const nav = event.target.closest('[data-nav]');
      if (nav) {
        const list = sortProjects(filteredProjects());
        const index = list.findIndex(function (project) { return project.id === state.projectId; });
        const target = nav.getAttribute('data-nav') === 'prev' ? list[index - 1] : list[index + 1];
        if (target) selectProject(target.id, true);
        return;
      }
      const corridorNav = event.target.closest('[data-corridor-nav]');
      if (corridorNav) {
        const index = corridors.findIndex(function (corridor) { return corridor.id === state.corridorId; });
        const target = corridorNav.getAttribute('data-corridor-nav') === 'prev' ? corridors[index - 1] : corridors[index + 1];
        if (target) selectCorridor(target.id, true);
      }
    });

    dom.viewPanel.addEventListener('click', function (event) {
      const corridor = event.target.closest('[data-corridor]');
      if (corridor) {
        selectCorridor(corridor.getAttribute('data-corridor'), true);
        return;
      }
      const estate = event.target.closest('[data-estate]');
      if (estate) {
        const id = estate.getAttribute('data-estate');
        const scrollTop = dom.viewPanel.scrollTop;
        state.expandedEstate = state.expandedEstate === id ? null : id;
        renderEstates();
        dom.viewPanel.scrollTop = scrollTop;
      }
    });

    dom.layerProjects.addEventListener('change', function () {
      if (window.AtlasMap) window.AtlasMap.setProjectsVisible(dom.layerProjects.checked);
    });
    dom.layerLabels.addEventListener('change', function () {
      if (window.AtlasMap) window.AtlasMap.setLabels(dom.layerLabels.checked);
    });

    document.addEventListener('keydown', function (event) {
      if (event.key !== 'Escape') return;
      if (!dom.filterPopover.hidden) {
        dom.filterPopover.hidden = true;
        dom.moreFilters.setAttribute('aria-expanded', 'false');
        dom.moreFilters.focus();
        return;
      }
      if (!dom.drawer.hidden) {
        if (state.projectId) closeProject();
        else closeCorridor();
      }
    });

    document.addEventListener('keydown', function (event) {
      if (event.key !== 'Tab' || dom.drawer.hidden) return;
      const focusable = dom.drawer.querySelectorAll('a[href], button:not([disabled]), input, select, textarea, [tabindex]:not([tabindex="-1"])');
      if (!focusable.length) return;
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    });

    window.addEventListener('popstate', applyRoute);
    window.addEventListener('hashchange', function () {
      if (location.hash !== lastHash) applyRoute();
    });
  }

  /* ---------- legend ---------- */

  function renderLegend() {
    dom.legendBody.innerHTML = STATUS_ORDER.map(function (status) {
      return '<div class="legend-row"><span class="dot" style="--c:' +
        esc((STATUS[status] && STATUS[status].color) || '#667085') + '"></span>' +
        esc(statusLabel(status)) + '</div>';
    }).join('') +
      '<div class="legend-sector">Marker glyph shows the sector: road, railway, airport, seaport or factory. Clusters show a status ring.</div>';
  }

  /* ---------- boot ---------- */

  function init() {
    dom.toast = $('toast');
    dom.search = $('search');
    dom.tabs = Array.from(document.querySelectorAll('[data-view]'));
    dom.rail = $('rail');
    dom.sheetHandle = $('sheet-handle');
    dom.exploreContent = $('explore-content');
    dom.viewPanel = $('view-panel');
    dom.sectorChips = $('sector-chips');
    dom.statusChips = $('status-chips');
    dom.activeFilters = $('active-filters');
    dom.filterBadge = $('filter-badge');
    dom.clearFilters = $('clear-filters');
    dom.moreFilters = $('more-filters');
    dom.filterPopover = $('filter-popover');
    dom.filterGrid = $('filter-grid');
    dom.popoverSummary = $('popover-summary');
    dom.popoverClose = $('popover-close');
    dom.resultCount = $('result-count');
    dom.sort = $('sort');
    dom.projectList = $('project-list');
    dom.footCount = $('foot-count');
    dom.footTotal = $('foot-total');
    dom.mapCount = $('map-count');
    dom.drawer = $('drawer');
    dom.drawerClose = $('drawer-close');
    dom.drawerPills = $('drawer-pills');
    dom.drawerTitle = $('drawer-title');
    dom.drawerLoc = $('drawer-loc');
    dom.drawerBody = $('drawer-body');
    dom.drawerFoot = $('drawer-foot');
    dom.statProjects = $('stat-projects');
    dom.statCorridors = $('stat-corridors');
    dom.statEstates = $('stat-estates');
    dom.tabCountExplore = $('tab-count-explore');
    dom.layerProjects = $('layer-projects');
    dom.layerLabels = $('layer-labels');
    dom.legendBody = $('legend-body');
    dom.mapWrap = document.querySelector('.map-wrap');

    if (!features.length) {
      dom.resultCount.textContent = 'Data not loaded';
      dom.projectList.innerHTML = '<li><div class="list-empty"><h3>No project data</h3>' +
        '<p>data/projects.js is missing or empty. Rebuild the site data.</p></div></li>';
      return;
    }

    renderLegend();
    renderFilterControls();
    bindEvents();
    bindSheet();

    if (window.AtlasMap) {
      window.AtlasMap.init({
        select: function (id) { selectProject(id, true); },
        deselect: function () {
          if (state.projectId) closeProject();
          else if (state.view === 'corridors' && state.corridorId) closeCorridor();
        }
      });
      window.AtlasMap.setProjects(projects);
    }

    parseHash();
    renderAll();
    initSheet();
    if (mobileQuery.matches) {
      const legend = document.querySelector('.map-legend');
      if (legend) legend.removeAttribute('open');
    }
    if (state.view === 'estates') ensureEstates();

    requestAnimationFrame(function () {
      if (window.AtlasMap) window.AtlasMap.resize();
      if (!state.projectId) {
        initialFitDone = true;
        window.AtlasMap && window.AtlasMap.fitAll(mobileQuery.matches ? dom.rail.offsetHeight + 16 : 8);
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
