/* Indonesia Infrastructure Atlas — application shell and views. */
(function () {
  'use strict';

  const A = window.ATLAS || {};
  const STATUS = A.STATUS || {};
  const STATUS_ORDER = A.STATUS_ORDER || [];
  const SECTORS = A.SECTORS || {};
  const SECTOR_ORDER = A.SECTOR_ORDER || [];
  const PROGRAMME_THEMES = A.PROGRAMME_THEMES || {};
  const PROGRAMME_THEME_ORDER = A.PROGRAMME_THEME_ORDER || [];
  const STALE_DAYS = A.STALE_DAYS || 183;
  const I18N = window.AtlasI18n || {};
  const EVENT_TYPES = [
    'announced', 'groundbreaking', 'contract', 'financial_close',
    'section_opened', 'opened', 'stalled', 'resumed', 'target_changed', 'other'
  ];
  const METRIC_KEYS = {
    'toll operational km': 'metric.toll_operational_km',
    'national road connected km': 'metric.national_road_connected_km',
    'route length; no current progress series': 'metric.route_length_no_current_series',
    'route length; no progress series': 'metric.route_length_no_series'
  };

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
  const searchCompanies = new Map(
    searchIndex.filter(function (entry) { return entry.type === 'company'; })
      .map(function (entry) { return [entry.id, entry]; })
  );

  let estates = window.INFRA_ESTATES || null;
  let estatesState = estates ? 'ready' : 'idle';
  let programmes = window.INFRA_PROGRAMMES || null;
  let programmesState = programmes ? 'ready' : 'idle';
  let pkpn = window.INFRA_PKPN || null;
  let companies = window.INFRA_COMPANIES || null;
  let companiesState = companies ? 'ready' : 'idle';

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
    expandedEstate: null,
    programmeTheme: 'all',
    companyType: 'all',
    companySort: 'name',
    expandedCompany: null,
    coverageSort: { key: '', dir: 1 }
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

  function t(key, vars) {
    return I18N.t ? I18N.t(key, vars) : key;
  }

  function tOr(key, fallback) {
    const value = t(key);
    return value === key ? fallback : value;
  }

  function fmtNum(value) {
    const number = Number(value);
    if (!isFinite(number)) return esc(value);
    return I18N.fmtNum ? I18N.fmtNum(number) : String(value);
  }

  // Investments are stored in trillions. Small commitments read better in
  // billions than as a rounded "Rp 0 T".
  function investmentParts(value) {
    const number = Number(value);
    if (!isFinite(number) || number === 0) return null;
    if (number >= 0.1) return [fmtNum(number), 'T'];
    return [fmtNum(number * 1000), 'B'];
  }

  function fmtInvestment(value) {
    const parts = investmentParts(value);
    return parts ? 'Rp ' + parts[0] + ' ' + parts[1] : '';
  }

  function fmtCoord(value) {
    const number = Number(value);
    if (!isFinite(number)) return esc(value);
    return I18N.fmtCoord ? I18N.fmtCoord(number) : String(value);
  }

  function fmtDate(value) {
    if (!value) return '';
    return I18N.fmtDate ? I18N.fmtDate(value) : String(value);
  }

  function projectName(project) {
    return I18N.entityName ? I18N.entityName('project', project) : project.name;
  }

  function corridorName(corridor) {
    return I18N.entityName ? I18N.entityName('corridor', corridor) : corridor.name;
  }

  function programmeName(programme) {
    if (I18N.entity) {
      return I18N.entity('programme', programme.id, 'name', programme.name_en || '');
    }
    return programme.name_en || programme.name_id || '';
  }

  function programmeField(programme, field) {
    if (I18N.entity) {
      return I18N.entity('programme', programme.id, field, '');
    }
    return '';
  }

  function corridorDefinition(corridor) {
    if (I18N.entity) {
      return I18N.entity('corridor', corridor.id, 'definition', corridor.definition || '');
    }
    return corridor.definition || '';
  }

  function provinceText(value) {
    return I18N.provinceName ? I18N.provinceName(value) : value;
  }

  function islandText(value) {
    return I18N.islandName ? I18N.islandName(value) : value;
  }

  function metricLabel(value) {
    const key = METRIC_KEYS[String(value || '').toLowerCase()];
    return key ? t(key) : value;
  }

  function localName(record) {
    if (I18N.locale === 'id') return record.name_id || record.name_en || '';
    return record.name_en || record.name_id || '';
  }

  function indicatorValue(value, unit) {
    if (String(unit).indexOf('Rp ') === 0) {
      const suffix = String(unit).slice(3);
      return 'Rp ' + fmtNum(value) + (suffix ? ' ' + suffix : '');
    }
    return fmtNum(value) + (unit ? ' ' + unit : '');
  }

  function indicatorSummary(indicator) {
    const values = indicator.values || [];
    const latest = values.length ? values[values.length - 1] : null;
    const unit = indicator.unit || '';
    const current = latest
      ? indicatorValue(latest.value, unit)
      : t('indicator.no_value');
    const target = indicator.target_value
      ? indicatorValue(indicator.target_value, unit)
      : '';
    const asOf = latest ? t('indicator.as_of', { date: fmtDate(latest.as_of) }) : '';
    const source = indicator.source_url
      ? ' <a href="' + esc(indicator.source_url) + '" target="_blank" rel="noopener">' +
        esc(t('action.open_source')) + '</a>'
      : '';
    return {
      name: localName(indicator),
      current: current,
      hasValue: !!latest,
      target: target,
      asOf: asOf,
      source: source
    };
  }

  function indicatorItems(indicators, compact) {
    return (indicators || []).map(function (indicator) {
      const info = indicatorSummary(indicator);
      const target = info.target
        ? ' · <b>' + esc(t('indicator.target')) + '</b> ' + esc(info.target)
        : '';
      const meta = [info.asOf].filter(Boolean).join(' ');
      const current = info.hasValue
        ? '<b>' + esc(t('indicator.current')) + '</b> ' + esc(info.current)
        : esc(t('indicator.no_value'));
      return '<li><time>' + esc(info.name) + '</time><span>' + current + target +
        (meta ? '<span class="indicator-meta">' + esc(meta) + info.source + '</span>' : info.source) +
        '</span></li>';
    }).join('');
  }

  function phaseItems(phases) {
    return (phases || []).map(function (phase) {
      const dates = [];
      if (phase.start_date) dates.push(t('phase.start') + ' ' + fmtDate(phase.start_date));
      if (phase.end_date) dates.push(t('phase.end') + ' ' + fmtDate(phase.end_date));
      const facts = [];
      if (phase.cost_idr_t) facts.push(t('phase.cost') + ' ' + fmtInvestment(phase.cost_idr_t));
      if (phase.progress_pct) facts.push(t('phase.progress') + ' ' + fmtNum(phase.progress_pct) + '%');
      const detail = dates.concat(facts).join(' · ');
      return '<li><time>' + esc(localName(phase)) + '</time><span><b>' +
        esc(statusLabel(phase.status)) + '</b>' + (detail ? ' · ' + esc(detail) : '') +
        (phase.source_url ? ' · <a href="' + esc(phase.source_url) + '" target="_blank" rel="noopener">' +
          esc(t('action.open_source')) + '</a>' : '') + '</span></li>';
    }).join('');
  }

  function daysSince(value) {
    if (!value) return Infinity;
    const parsed = new Date(value + 'T00:00:00');
    if (isNaN(parsed.getTime())) return Infinity;
    const base = stats.data_as_of ? new Date(stats.data_as_of + 'T00:00:00') : new Date();
    return Math.floor((base.getTime() - parsed.getTime()) / 86400000);
  }

  function isStale(value) {
    return daysSince(value) > STALE_DAYS;
  }

  function freshnessLabel(state) {
    return t('freshness.' + (state || 'unknown'));
  }

  function statusLabel(status) {
    if (!status) return t('status.unknown.label');
    return tOr('status.' + status + '.label', status);
  }

  function statusShort(status) {
    if (!status) return t('status.unknown.short');
    return tOr('status.' + status + '.short', statusLabel(status));
  }

  function eventLabel(type) {
    return EVENT_TYPES.indexOf(type) === -1 ? t('event.other') : t('event.' + type);
  }

  function sectorLabel(sector, plural) {
    if (!sector) return '';
    return tOr('sector.' + sector + (plural ? '.plural' : '.label'), sector);
  }

  function sectorShort(sector) {
    return tOr('sector.' + sector + '.short', sectorLabel(sector, true));
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
    const list = splitProvinces(project.province).map(provinceText);
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

  const SEARCH_ALIASES = {
    tol: ['toll'], toll: ['tol'],
    bandara: ['airport'], airport: ['bandara'],
    pelabuhan: ['port', 'seaport'], port: ['pelabuhan'], seaport: ['pelabuhan'],
    kereta: ['railway'], railway: ['kereta'],
    bendungan: ['dam'], dam: ['bendungan'],
    jalan: ['road'], road: ['jalan'],
    pabrik: ['factory'], factory: ['pabrik'],
    energi: ['energy'], energy: ['energi'],
    air: ['water'], water: ['air'],
    perumahan: ['housing'], housing: ['perumahan'],
    pendidikan: ['education'], education: ['pendidikan'],
    pariwisata: ['tourism'], tourism: ['pariwisata'],
    pertanian: ['agriculture'], agriculture: ['pertanian'],
    proyek: ['project'], project: ['proyek'],
    program: ['programme'], programme: ['program'],
    perusahaan: ['company'], company: ['perusahaan'],
    koridor: ['corridor'], corridor: ['koridor'],
    kek: ['sez'], sez: ['kek']
  };

  function tokenMatches(haystack, token) {
    if (haystack.indexOf(token) !== -1) return true;
    return (SEARCH_ALIASES[token] || []).some(function (alias) {
      return haystack.indexOf(alias) !== -1;
    });
  }

  function matchesHaystack(haystack, query) {
    if (!query) return true;
    return query.toLowerCase().split(/\s+/).filter(Boolean).every(function (token) {
      return tokenMatches(haystack, token);
    });
  }

  function matchesQuery(project, query) {
    if (!query) return true;
    const entry = searchProjects.get(project.id);
    const haystack = (entry ? entry.text : [
      project.name, project.province, project.island, project.route, project.operator,
      project.subsector, project.corridor_name,
      sectorLabel(project.sector), statusLabel(project.status),
      project.psn === 'yes' ? 'psn' : ''
    ].join(' ')).toLowerCase();
    return matchesHaystack(haystack, query);
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
    state.companyType = params.get('ctype') || 'all';
    state.companySort = params.get('csort') || 'name';
    state.expandedCompany = null;

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
    } else if (view === 'programmes') {
      state.view = 'programmes';
    } else if (view === 'companies') {
      state.view = 'companies';
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
    if (state.view === 'companies') {
      if (state.companyType !== 'all') params.set('ctype', state.companyType);
      if (state.companySort !== 'name') params.set('csort', state.companySort);
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
    if (state.view === 'programmes') ensureProgrammes();
    if (state.view === 'companies') ensureCompanies();
  }

  function applyRoute() {
    parseHash();
    renderAll();
    if (state.view === 'estates') ensureEstates();
    if (state.view === 'programmes') ensureProgrammes();
    if (state.view === 'companies') ensureCompanies();
    if (mobileQuery.matches) setSheetHeight(sheetSnapForView());
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
    const totalEstates = (stats.estates && stats.estates.total) || (estates ? estates.length : 0);
    dom.statProjects.textContent = fmtNum(totalProjects);
    dom.statCorridors.textContent = fmtNum(totalCorridors);
    dom.statEstates.textContent = fmtNum(totalEstates);
    if (dom.search.value !== state.q) dom.search.value = state.q;
    dom.tabCountExplore.textContent = fmtNum(totalProjects);
    if (dom.tabCountProgrammes) {
      dom.tabCountProgrammes.textContent = fmtNum((stats.programmes && stats.programmes.total) || 24);
    }
    if (dom.tabCountCompanies) {
      dom.tabCountCompanies.textContent = fmtNum((stats.organizations && stats.organizations.total) || 101);
    }
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
      esc(t('filter.all')) + '<span class="chip-count">' + fmtNum(projects.filter(function (project) {
        return passesFilters(project, { skipSector: true });
      }).length) + '</span></button>';
    SECTOR_ORDER.forEach(function (sector) {
      const count = counts[sector] || 0;
      const pressed = state.filters.sectors.has(sector);
      const short = sectorShort(sector);
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
      const short = statusShort(status);
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
    if (state.filters.island) chips.push({ key: 'island', label: islandText(state.filters.island) });
    if (state.filters.province) chips.push({ key: 'province', label: provinceText(state.filters.province) });
    if (state.filters.psn) {
      chips.push({
        key: 'psn',
        label: t('filter.psn_value', {
          value: state.filters.psn === 'yes' ? 'PSN' : state.filters.psn === 'no'
            ? t('filter.not_psn') : t('filter.unknown')
        })
      });
    }
    if (state.filters.corridor) {
      const corridor = corridorById.get(state.filters.corridor);
      chips.push({ key: 'corridor', label: corridor ? corridorName(corridor) : state.filters.corridor });
    }
    if (state.filters.precision) {
      chips.push({
        key: 'precision',
        label: t('filter.precision_value', {
          value: tOr('filter.' + state.filters.precision, state.filters.precision)
        })
      });
    }
    if (state.filters.freshness) {
      chips.push({
        key: 'freshness',
        label: state.filters.freshness === 'fresh' ? t('freshness.fresh_short') : t('filter.stale')
      });
    }

    if (!chips.length) {
      dom.activeFilters.hidden = true;
      dom.activeFilters.innerHTML = '';
    } else {
      dom.activeFilters.hidden = false;
      dom.activeFilters.innerHTML = chips.map(function (chip) {
        return '<span class="active-filter">' + esc(chip.label) +
          '<button type="button" data-remove="' + esc(chip.key) + '" aria-label="' +
          esc(t('filter.remove', { name: chip.label })) + '">&times;</button></span>';
      }).join('');
    }

    const count = activeFilterCount();
    dom.filterBadge.hidden = count === 0;
    dom.filterBadge.textContent = String(count);
    dom.clearFilters.hidden = !hasAnyFilter();
    dom.popoverSummary.textContent = t('filter.match', {
      count: fmtNum(filteredProjects().length), total: fmtNum(projects.length)
    });
  }

  function filterOptions(placeholder, entries) {
    return '<option value="">' + esc(placeholder) + '</option>' + entries.map(function (entry) {
      return '<option value="' + esc(entry.value) + '">' + esc(entry.label) + '</option>';
    }).join('');
  }

  function renderFilterControls() {
    if (!dom.filterGrid) return;
    const islandOptions = filterOptions(
      t('filter.any_island'),
      ((stats.projects && stats.projects.island) ? Object.keys(stats.projects.island) : [])
        .sort().map(function (island) {
          return { value: island, label: islandText(island) };
        })
    );
    const provinceOptions = filterOptions(
      t('filter.any_province'),
      ((stats.projects && stats.projects.by_province) ? Object.keys(stats.projects.by_province) : [])
        .sort().map(function (province) {
          return { value: province, label: provinceText(province) };
        })
    );
    const corridorOptions = filterOptions(
      t('filter.any_corridor'),
      corridors.map(function (corridor) {
        return { value: corridor.id, label: corridorName(corridor) };
      })
    );

    dom.filterGrid.innerHTML =
      '<div class="field"><label for="f-island">' + esc(t('filter.island')) + '</label><select id="f-island" data-filter="island">' + islandOptions + '</select></div>' +
      '<div class="field"><label for="f-province">' + esc(t('filter.province')) + '</label><select id="f-province" data-filter="province">' + provinceOptions + '</select></div>' +
      '<div class="field"><label for="f-psn">' + esc(t('filter.psn')) + '</label><select id="f-psn" data-filter="psn">' +
        filterOptions(t('filter.any'), [
          { value: 'yes', label: 'PSN' },
          { value: 'no', label: t('filter.not_psn') },
          { value: 'unknown', label: t('filter.unknown') }
        ]) + '</select></div>' +
      '<div class="field"><label for="f-corridor">' + esc(t('filter.corridor')) + '</label><select id="f-corridor" data-filter="corridor">' + corridorOptions + '</select></div>' +
      '<div class="field"><label for="f-precision">' + esc(t('filter.precision')) + '</label><select id="f-precision" data-filter="precision">' +
        filterOptions(t('filter.any'), [
          { value: 'exact', label: t('filter.exact') },
          { value: 'approximate', label: t('filter.approximate') },
          { value: 'regency', label: t('filter.regency') },
          { value: 'province', label: t('filter.province_precision') }
        ]) + '</select></div>' +
      '<div class="field"><label for="f-fresh">' + esc(t('filter.verification')) + '</label><select id="f-fresh" data-filter="freshness">' +
        filterOptions(t('filter.any_date'), [
          { value: 'fresh', label: t('filter.under_6_months') },
          { value: 'stale', label: t('filter.stale') }
        ]) + '</select></div>';

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
    if (project.operational_km) bits.push(t('row.km_open', { value: fmtNum(project.operational_km) }));
    if (!bits.length && project.investment_idr_t) bits.push(fmtInvestment(project.investment_idr_t));
    if (!bits.length && project.capacity) bits.push(fmtNum(project.capacity) + ' ' + (I18N.unitLabel ? I18N.unitLabel(project.capacity_unit) : project.capacity_unit));
    if (!bits.length && project.opened_year) bits.push(t('row.opened', { year: project.opened_year }));
    if (!bits.length && project.expected_open_year) bits.push(t('row.target', { year: project.expected_open_year }));
    return bits.join(' · ') || t('row.no_figure');
  }

  function renderProjectRows(list) {
    if (!list.length) {
      dom.projectList.innerHTML = '<li><div class="list-empty">' +
        '<svg aria-hidden="true"><use href="#i-search"></use></svg>' +
        '<h3>' + esc(t('result.no_match_title')) + '</h3>' +
        '<p>' + esc(t('result.no_match_body')) + '</p>' +
        '<button class="filter-button" id="empty-clear" type="button">' + esc(t('result.clear_filters')) + '</button>' +
        '</div></li>';
      const clear = $('empty-clear');
      if (clear) clear.addEventListener('click', function () { resetFilters(); state.q = ''; commit(false); });
      return;
    }

    dom.projectList.innerHTML = list.map(function (project) {
      const share = project.progress_pct ? Number(project.progress_pct) : openShare(project);
      const shareLabel = project.progress_pct ? t('row.built', { value: fmtNum(project.progress_pct) }) :
        (share !== null ? t('row.open_pct', { value: fmtNum(share) }) : '');
      const current = state.projectId === project.id ? 'true' : 'false';
      const psn = project.psn === 'yes' ? ' · ' + t('row.psn') : '';
      const name = projectName(project);
      const sub = provinceShort(project) + ' · ' + sectorLabel(project.sector) + psn;
      return '<li><button type="button" class="project-row" data-project="' + esc(project.id) +
        '" aria-current="' + current + '" aria-label="' + esc(name + ', ' +
        statusLabel(project.status) + ', ' + provinceShort(project)) + '">' +
        '<span class="row-status" style="--c:' + esc((STATUS[project.status] && STATUS[project.status].color) || '#667085') + '"></span>' +
        '<span class="row-icon">' + sectorIcon(project.sector, 13) + '</span>' +
        '<span class="row-main">' +
        '<span class="row-line"><span class="row-title">' + esc(name) + '</span>' +
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

  function searchGroupCounts() {
    const counts = { project: 0, programme: 0, corridor: 0, estate: 0, company: 0 };
    const query = state.q.trim();
    if (!query) return counts;
    searchIndex.forEach(function (entry) {
      if (entry.text && matchesHaystack(entry.text.toLowerCase(), query)) {
        counts[entry.type] = (counts[entry.type] || 0) + 1;
      }
    });
    return counts;
  }

  function renderSearchGroups() {
    if (!dom.searchGroups) return;
    const query = state.q.trim();
    if (!query) {
      dom.searchGroups.hidden = true;
      dom.searchGroups.innerHTML = '';
      return;
    }
    const counts = searchGroupCounts();
    const groups = [
      ['project', t('search.projects'), 'explore'],
      ['programme', t('search.programmes'), 'programmes'],
      ['corridor', t('search.corridors'), 'corridors'],
      ['estate', t('search.estates'), 'estates'],
      ['company', t('search.companies'), 'companies']
    ];
    dom.searchGroups.hidden = false;
    if (!groups.some(function (group) { return counts[group[0]]; })) {
      dom.searchGroups.innerHTML = '<span class="search-groups-empty">' +
        esc(t('search.no_results')) + '</span>';
      return;
    }
    dom.searchGroups.innerHTML = groups.map(function (group) {
      const count = counts[group[0]] || 0;
      return '<button type="button" class="search-group' + (count ? '' : ' is-empty') +
        '" data-search-view="' + group[2] + '" data-search-type="' + group[0] + '"' +
        (count ? '' : ' disabled') + '>' + esc(group[1]) +
        '<span class="chip-count">' + fmtNum(count) + '</span></button>';
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
    renderSearchGroups();
    syncFilterControls();

    dom.resultCount.innerHTML = list.length === total
      ? t('result.projects', { count: fmtNum(total) })
      : t('result.of_projects', { count: fmtNum(list.length), total: fmtNum(total) });
    dom.footCount.textContent = fmtNum(list.length);
    dom.footTotal.textContent = fmtNum(total);
    dom.mapCount.textContent = fmtNum(list.filter(isMapped).length);
    if (dom.mapCaptionText) dom.mapCaptionText.textContent = t('map.caption');
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

  function untranslated(text) {
    if (!text) return '';
    if (I18N.locale === 'id') {
      return '<span class="lang-tag" title="' + esc(t('app.translation_pending')) + '">EN</span> ' +
        '<span lang="en">' + esc(text) + '</span>';
    }
    return esc(text);
  }

  function claimLabel(value) {
    return String(value || '').split(',').map(function (part) {
      const key = part.trim();
      return key ? tOr('claim.' + key, key) : '';
    }).filter(Boolean).join(', ');
  }

  function projectMetrics(project) {
    const metrics = [];
    if (project.length_km) metrics.push(metricCard(t('drawer.metric.corridor_length'), fmtNum(project.length_km) + ' <small>km</small>'));
    if (project.operational_km) metrics.push(metricCard(t('drawer.metric.open'), fmtNum(project.operational_km) + ' <small>km</small>'));
    if (project.construction_km) metrics.push(metricCard(t('drawer.metric.under_construction'), fmtNum(project.construction_km) + ' <small>km</small>'));
    if (project.investment_idr_t) {
      const inv = investmentParts(project.investment_idr_t);
      if (inv) metrics.push(metricCard(t('drawer.metric.investment'), 'Rp ' + inv[0] + ' <small>' + inv[1] + '</small>'));
    }
    if (project.capacity) metrics.push(metricCard(t('drawer.metric.capacity'), fmtNum(project.capacity) + ' <small>' + esc(I18N.unitLabel ? I18N.unitLabel(project.capacity_unit) : project.capacity_unit) + '</small>'));
    if (project.opened_year) metrics.push(metricCard(t('drawer.metric.opened'), esc(project.opened_year)));
    if (metrics.length < 2) metrics.push(metricCard(t('drawer.metric.psn'), esc(project.psn === 'yes' ? t('drawer.metric.yes') : project.psn === 'no' ? t('drawer.metric.no') : t('drawer.metric.unknown'))));
    if (metrics.length < 2) metrics.push(metricCard(t('drawer.metric.last_verified'), esc(fmtDate(project.last_verified))));
    return metrics.slice(0, 4).join('');
  }

  function projectSourceList(project) {
    const sources = project.sources || [];
    if (!sources.length) {
      return '<p class="basis">' + esc(t('drawer.no_source')) + '</p>';
    }
    return '<ul class="source-list">' + sources.map(function (source) {
      const claim = source.claim ? ' · ' + esc(claimLabel(source.claim)) : '';
      const published = source.published_on ? ' · ' + esc(t('drawer.published')) + ' ' + esc(fmtDate(source.published_on)) : '';
      return '<li><div class="src-head"><span class="src-name">' + esc(source.title || source.publisher) +
        '</span><span class="src-type">' + esc(tOr('data.source_type.' + (source.source_type || 'source'), source.source_type || 'source')) + '</span></div>' +
        '<div class="src-meta">' + esc(source.publisher) + claim + ' · ' + esc(t('drawer.retrieved')) + ' ' +
        esc(fmtDate(source.retrieved_on)) + published + '</div>' +
        (source.url ? '<a href="' + esc(source.url) + '" target="_blank" rel="noopener">' + esc(t('action.open_source')) + '</a>' : '') +
        '</li>';
    }).join('') + '</ul>';
  }

  function renderProjectDrawer(project) {
    const name = projectName(project);
    dom.drawerPills.innerHTML = statusPill(project.status) + sectorPill(project.sector);
    dom.drawerTitle.textContent = name;
    dom.drawerLoc.textContent = provinceText(project.province) + ' · ' + project.route;

    const basisSource = (project.sources && project.sources[0]) || null;
    const share = project.progress_pct ? Number(project.progress_pct) : openShare(project);
    const shareLabel = project.progress_pct ? t('drawer.reported_progress') : t('drawer.operational_share');

    let body = '';
    if (I18N.locale === 'id') {
      body += '<p class="translation-note">' + esc(t('language.note')) + '</p>';
    }
    body += '<div class="metric-grid">' + projectMetrics(project) + '</div>';

    if (share !== null && isFinite(share)) {
      body += '<div class="progress-block"><div class="progress-head"><span>' + esc(shareLabel) +
        '</span><strong>' + fmtNum(share) + '%</strong></div><div class="progress-track">' +
        '<span style="width:' + Math.max(0, Math.min(100, share)) + '%;--c:' +
        esc((STATUS[project.status] && STATUS[project.status].color) || '#c2410c') + '"></span></div></div>';
    }

    const summary = I18N.entity ? I18N.entity('project', project.id, 'summary', '') : '';
    if (summary) {
      const generated = I18N.entity('project', project.id, 'summary_state', '') === 'generated';
      body += '<section class="detail-section project-summary"><h3>' + esc(t('drawer.summary')) + '</h3><p>' +
        esc(summary) + (generated ? ' <span class="lang-tag" title="' +
          esc(t('drawer.summary_generated')) + '">' + esc(t('drawer.auto_tag')) + '</span>' : '') +
        '</p></section>';
    }

    if (project.indicators && project.indicators.length) {
      body += '<section class="detail-section"><h3>' + esc(t('drawer.indicators')) +
        '</h3><ul class="evidence-list">' + indicatorItems(project.indicators) + '</ul></section>';
    }
    if (project.phases && project.phases.length) {
      body += '<section class="detail-section"><h3>' + esc(t('drawer.phases')) +
        '</h3><ul class="evidence-list">' + phaseItems(project.phases) + '</ul></section>';
    }

    body += '<section class="detail-section"><h3>' + esc(t('drawer.why_status')) + '</h3>' +
      '<p class="basis">' + untranslated(project.status_basis) + '</p>' +
      '<div class="basis-meta">' + esc(t('drawer.status_as_of', {
        date: fmtDate(project.status_as_of || project.last_verified)
      })) + (basisSource ? ' · ' + esc(basisSource.publisher) : '') + '</div></section>';

    body += '<section class="detail-section"><h3>' + esc(t('drawer.evidence')) + '</h3><ul class="evidence-list">' +
      '<li><time>' + esc(fmtDate(project.last_verified)) + '</time><span>' + esc(t('drawer.record_verified')) +
      (basisSource ? esc(t('drawer.against', { title: basisSource.title })) : '') + '.</span></li>' +
      (project.opened_year ? '<li><time>' + esc(project.opened_year) + '</time><span>' + esc(t('drawer.opened_service')) + '</span></li>' : '') +
      (project.corridor_name ? '<li><time>' + esc(t('drawer.corridor')) + '</time><span>' +
        esc(t('drawer.part_of', { name: project.corridor_name })) +
        ' <a class="related-link" href="#/corridors/' + esc(project.corridor_id) + '">' + esc(t('action.open_corridor')) + '</a></span></li>' : '') +
      '</ul></section>';

    if (project.events && project.events.length) {
      body += '<section class="detail-section"><h3>' + esc(t('drawer.timeline')) + '</h3>' +
        '<ul class="evidence-list event-list">' + project.events.map(function (event) {
          return '<li><time>' + esc(fmtDate(event.event_date)) + '</time><span><b>' +
            esc(eventLabel(event.event_type)) + '</b> · ' + untranslated(event.description) +
            (event.source_url ? ' <a href="' + esc(event.source_url) + '" target="_blank" rel="noopener">' + esc(t('corridor.source')) + ' ↗</a>' : '') +
            '</span></li>';
        }).join('') + '</ul></section>';
    }

    body += '<section class="detail-section"><h3>' + esc(t('drawer.sources')) + '</h3>' + projectSourceList(project) + '</section>';

    if (project.notes) {
      body += '<section class="detail-section"><h3>' + esc(t('drawer.notes_conflicts')) + '</h3>' +
        '<p class="notes-callout">' + untranslated(project.notes) + '</p></section>';
    }

    const coordinateNote = project.precision === 'province'
      ? t('drawer.province_centroid')
      : t('drawer.precision', { value: tOr('filter.' + project.precision, project.precision) });
    body += '<section class="detail-section"><h3>' + esc(t('drawer.data_quality')) + '</h3><ul class="evidence-list">' +
      '<li><time>' + esc(t('drawer.coordinates')) + '</time><span>' + esc(coordinateNote) + ' · ' +
      fmtCoord(project.lat) + ', ' + fmtCoord(project.lon) + '</span></li>' +
      '<li><time>' + esc(t('drawer.psn')) + '</time><span>' + esc(project.psn === 'yes' ? t('drawer.psn_yes') :
        project.psn === 'no' ? t('drawer.psn_no') : t('drawer.psn_unknown')) + '</span></li>' +
      '<li><time>' + esc(t('drawer.verification')) + '</time><span>' + esc(tOr('verification.' + project.verification, project.verification)) +
      ' · ' + esc(t('drawer.status_as_of', { date: fmtDate(project.status_as_of) })) + '</span></li>' +
      ((project.aliases && project.aliases.length)
        ? '<li><time>' + esc(t('drawer.official_name')) + '</time><span>' + esc(project.aliases.join('; ')) + '</span></li>'
        : '') +
      (project.verification === 'unverified' && project.status === 'unknown'
        ? '<li><time>' + esc(t('drawer.record')) + '</time><span>' + esc(t('drawer.register_only')) + '</span></li>'
        : '') +
      '<li><time>' + esc(t('drawer.freshness')) + '</time><span class="freshness-line"><span class="freshness-dot ' +
      esc(project.freshness_state || 'unknown') + '"></span>' +
      esc(freshnessLabel(project.freshness_state)) + ' · ' +
      esc(t('drawer.due', { date: fmtDate(project.freshness_due) })) + '</span></li>' +
      '<li><time>' + esc(t('drawer.record')) + '</time><span>' + esc(project.id) + '</span></li>' +
      '</ul></section>';

    dom.drawerBody.innerHTML = body;
    dom.drawerBody.scrollTop = 0;

    const list = sortProjects(filteredProjects());
    const index = list.findIndex(function (item) { return item.id === project.id; });
    const prev = index > 0 ? list[index - 1] : null;
    const next = index !== -1 && index < list.length - 1 ? list[index + 1] : null;

    dom.drawerFoot.innerHTML =
      '<div class="drawer-meta"><span>' + esc(t('drawer.precision_coordinates', {
        value: tOr('filter.' + project.precision, project.precision)
      })) + '</span>' +
      '<span>' + esc(t('drawer.verified', { date: fmtDate(project.last_verified) })) + '</span>' +
      '<span>' + esc(project.id) + '</span></div>' +
      '<div class="drawer-nav">' +
      '<button class="nav-btn" type="button" data-nav="prev"' + (prev ? '' : ' disabled') + '>' +
      '<svg aria-hidden="true"><use href="#i-chevron-left"></use></svg>' + (prev ? esc(projectName(prev)) : esc(t('action.previous'))) + '</button>' +
      '<button class="share-btn" type="button" data-share="' + esc(project.id) + '">' +
      '<svg width="11" height="11" aria-hidden="true"><use href="#i-share"></use></svg> ' + esc(t('action.share')) + '</button>' +
      '<button class="nav-btn" type="button" data-nav="next"' + (next ? '' : ' disabled') + '>' +
      (next ? esc(projectName(next)) : esc(t('action.next'))) + '<svg aria-hidden="true"><use href="#i-chevron-right"></use></svg></button>' +
      '</div>';

    dom.drawer.dataset.kind = 'project';
    dom.drawer.dataset.id = project.id;
    openDrawer();
  }

  function corridorSegmentTable(corridor) {
    const segments = corridor.segments || [];
    if (!segments.length) {
      return '<p class="basis">' + esc(t('corridor.no_segments')) + '</p>';
    }
    return '<div class="segment-wrap"><table class="segment-table"><thead><tr>' +
      '<th scope="col">' + esc(t('corridor.section')) + '</th><th scope="col">' + esc(t('corridor.length')) +
      '</th><th scope="col">' + esc(t('corridor.status')) + '</th><th scope="col">' + esc(t('corridor.opened')) + '</th>' +
      '</tr></thead><tbody>' + segments.map(function (segment) {
        const color = (STATUS[segment.status] && STATUS[segment.status].color) || '#667085';
        const note = segment.notes ? '<span class="segment-note">' + untranslated(segment.notes) + '</span>' : '';
        const opened = segment.opened_year ? esc(segment.opened_year) :
          (segment.expected_open_year ? esc(t('corridor.by_year', { year: segment.expected_open_year })) : '—');
        return '<tr><th scope="row">' + esc(segment.name) + note + '</th>' +
          '<td class="num">' + fmtNum(segment.length_km) + ' km</td>' +
          '<td><span class="status-dot" style="--c:' + esc(color) + '"></span>' + esc(statusLabel(segment.status)) + '</td>' +
          '<td class="num">' + opened + '</td></tr>';
      }).join('') + '</tbody></table></div>';
  }

  function corridorTimeline(corridor) {
    const events = corridor.events || [];
    if (!events.length) {
      return '<p class="basis">' + esc(t('corridor.no_events')) + '</p>';
    }
    const groups = [];
    events.forEach(function (event) {
      const year = String(event.event_date || '').slice(0, 4) || t('corridor.undated');
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
            esc(event.project_name) + '. ' + untranslated(event.description) +
            (event.source_url ? ' <a href="' + esc(event.source_url) + '" target="_blank" rel="noopener">' + esc(t('corridor.source')) + ' ↗</a>' : '') +
            '</div></li>';
        }).join('') + '</ul></li>';
    }).join('') + '</ol>';
  }

  function renderCorridorDrawer(corridor) {
    const definition = corridorDefinition(corridor);
    dom.drawerPills.innerHTML = '<span class="status-pill plain">' + esc(t('corridor.trans_corridor')) + '</span>' +
      '<span class="status-pill plain">' + esc(islandText(corridor.island)) + '</span>';
    dom.drawerTitle.textContent = corridorName(corridor);
    dom.drawerLoc.textContent = definition;

    const parts = corridorParts(corridor);
    const word = corridorWord(corridor);
    const metricTitle = word === 'connected' ? t('corridor.connected') : word === 'paved' ? t('corridor.paved') : t('corridor.operating');
    const share = parts.hasTotal && parts.operational ? (parts.operational / parts.total) * 100 : null;
    const remaining = parts.hasTotal && (parts.operational || parts.construction)
      ? Math.max(parts.total - parts.operational - parts.construction, 0)
      : null;
    const segments = corridor.segments || [];
    const segmentKm = Number(corridor.segment_km) || 0;
    const state = corridorState(corridor);

    let body = '<div class="metric-grid">';
    body += metricCard(t('corridor.total'), parts.hasTotal ? fmtNum(parts.total) + ' <small>km</small>' : t('corridor.not_defined'));
    body += metricCard(metricTitle, parts.operational ? fmtNum(parts.operational) + ' <small>km</small>' : '—');
    body += metricCard(t('corridor.under_construction'), parts.construction ? fmtNum(parts.construction) + ' <small>km</small>' : '—');
    body += metricCard(t('corridor.not_yet_open'), remaining ? fmtNum(remaining) + ' <small>km</small>' : '—');
    body += '</div>';

    if (parts.hasTotal && hasBreakdown(parts)) {
      body += corridorBar(corridor) + corridorLegend(corridor);
    }

    if (share !== null) {
      body += '<div class="progress-block"><div class="progress-head"><span>' + esc(metricLabel(corridor.metric)) +
        '</span><strong>' + fmtNum(share) + '%</strong></div><div class="progress-track">' +
        '<span style="width:' + pctOf(parts.operational, parts.total) +
        '%;--c:var(--operating)"></span></div></div>';
    }

    body += '<section class="detail-section"><h3>' + esc(t('corridor.definition_scope')) + '</h3><p class="basis">' +
      esc(definition) + '</p><div class="basis-meta">' + esc(t('corridor.metric')) + ': ' + esc(metricLabel(corridor.metric)) +
      (corridor.as_of ? ' · ' + esc(t('corridor.as_of', { date: fmtDate(corridor.as_of) })) : '') + '</div></section>';

    body += '<section class="detail-section"><h3>' + esc(t('corridor.series_coverage')) + '</h3><p class="basis">' +
      (segments.length
        ? esc(t('corridor.sections_covering', { count: segments.length, km: fmtNum(segmentKm) })) +
          (parts.hasTotal ? esc(t('corridor.of_route_total', { pct: fmtNum(corridor.segment_share) })) : '') + '. ' +
          esc(state.key === 'partial' ? t('corridor.partial_note') : t('corridor.reconcile_note'))
        : esc(t('corridor.no_segment_note'))) +
      '</p><div class="basis-meta"><span class="corridor-state ' + esc(state.key) + '">' +
      esc(state.label) + '</span></div></section>';

    if (corridor.notes) {
      body += '<section class="detail-section"><h3>' + esc(t('drawer.notes_conflicts')) + '</h3><p class="notes-callout">' +
        untranslated(corridor.notes) + '</p></section>';
    }

    body += '<section class="detail-section"><h3>' + esc(t('corridor.segments')) + '</h3>' + corridorSegmentTable(corridor) + '</section>';
    body += '<section class="detail-section"><h3>' + esc(t('corridor.timeline')) + '</h3>' + corridorTimeline(corridor) + '</section>';

    body += '<section class="detail-section"><h3>' + esc(t('corridor.source')) + '</h3><ul class="source-list"><li>' +
      '<div class="src-head"><span class="src-name">' + esc(corridor.source_title || corridor.source_publisher) +
      '</span><span class="src-type">' + esc(tOr('data.source_type.' + (corridor.source_type || 'source'), corridor.source_type || 'source')) + '</span></div>' +
      '<div class="src-meta">' + esc(corridor.source_publisher) + ' · ' + esc(t('drawer.retrieved')) + ' ' +
      esc(fmtDate(corridor.retrieved_on)) + '</div>' +
      (corridor.source_url ? '<a href="' + esc(corridor.source_url) + '" target="_blank" rel="noopener">' + esc(t('action.open_source')) + '</a>' : '') +
      '</li></ul></section>';

    dom.drawerBody.innerHTML = body;
    dom.drawerBody.scrollTop = 0;

    const index = corridors.findIndex(function (item) { return item.id === corridor.id; });
    dom.drawerFoot.innerHTML =
      '<div class="drawer-meta"><span>' + esc(t('corridor.metric_aria', { metric: metricLabel(corridor.metric) })) + '</span>' +
      (corridor.as_of ? '<span>' + esc(t('corridor.as_of', { date: fmtDate(corridor.as_of) })) + '</span>' : '') +
      '<span>' + esc(corridor.id) + '</span></div>' +
      '<div class="drawer-nav">' +
      '<button class="nav-btn" type="button" data-corridor-nav="prev"' + (index > 0 ? '' : ' disabled') + '>' +
      '<svg aria-hidden="true"><use href="#i-chevron-left"></use></svg>' + esc(t('action.previous')) + '</button>' +
      '<button class="share-btn" type="button" data-share="' + esc(corridor.id) + '">' +
      '<svg width="11" height="11" aria-hidden="true"><use href="#i-share"></use></svg> ' + esc(t('action.share')) + '</button>' +
      '<button class="nav-btn" type="button" data-corridor-nav="next"' +
      (index !== -1 && index < corridors.length - 1 ? '' : ' disabled') + '>' + esc(t('action.next')) +
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

  function isMapped(project) {
    return project.precision !== 'province';
  }

  function renderMap() {
    if (!window.AtlasMap) return;
    const list = filteredProjects();
    const mapped = list.filter(isMapped);
    window.AtlasMap.setProjects(mapped);
    dom.mapCount.textContent = fmtNum(mapped.length);
    if (dom.mapCaptionText) dom.mapCaptionText.textContent = t('map.caption');

    if (state.projectId && projectById.has(state.projectId) &&
        list.some(function (project) { return project.id === state.projectId; }) &&
        isMapped(projectById.get(state.projectId))) {
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
    if (!parts.hasTotal) return { key: 'none', label: t('corridor.state.none') };
    if (!parts.operational) return { key: 'total', label: t('corridor.state.total') };
    const share = Number(corridor.segment_share);
    if (corridor.segment_share !== null && corridor.segment_share !== undefined && isFinite(share) && share < 99.5) {
      return { key: 'partial', label: t('corridor.state.partial') };
    }
    return { key: 'full', label: t('corridor.state.full') };
  }

  function filteredCorridors() {
    const query = state.q.trim();
    if (!query) return corridors;
    return corridors.filter(function (corridor) {
      return matchesHaystack(
        [corridor.name, corridor.definition, corridor.island, corridor.metric]
          .join(' ').toLowerCase(),
        query
      );
    });
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
      figure = '<strong>' + fmtNum(parts.operational) + '</strong> ' + esc(t('footer.of')) + ' ' + fmtNum(parts.total) + ' km ' + esc(word);
    } else if (parts.hasTotal) {
      figure = '<strong>' + fmtNum(parts.total) + ' km</strong> ' + esc(t('corridor.no_progress_series'));
    } else {
      figure = '<strong>' + esc(t('corridor.state.none')) + '</strong> · ' + esc(t('corridor.aggregate_withheld'));
    }

    let meta = '';
    if (share !== null) meta = fmtNum(share) + '% ' + word;
    else if (parts.hasTotal) meta = t('corridor.route_total_only');
    if (corridor.as_of) meta += (meta ? ' · ' : '') + t('corridor.as_of', { date: fmtDate(corridor.as_of) });

    const coverage = segments.length
      ? t('corridor.sections_meta', { count: segments.length, km: fmtNum(segmentKm) }) +
        (parts.hasTotal && segmentKm ? t('corridor.of_route_short', { pct: fmtNum(corridor.segment_share) }) : '')
      : t('corridor.no_segment_table');

    return '<button type="button" class="corridor-card" data-corridor="' + esc(corridor.id) + '">' +
      '<div class="corridor-head"><h3>' + esc(corridorName(corridor)) + '</h3>' +
      '<span class="corridor-metric">' + esc(metricLabel(corridor.metric)) + '</span></div>' +
      '<div class="corridor-figure">' + figure + '</div>' +
      (meta ? '<div class="corridor-meta">' + esc(meta) + '</div>' : '') +
      '<p class="corridor-def">' + esc(corridorDefinition(corridor)) + '</p>' +
      (hasBreakdown(parts) ? corridorBar(corridor) + corridorLegend(corridor) : '') +
      '<div class="corridor-foot"><span class="corridor-state ' + esc(state.key) + '">' + esc(state.label) + '</span>' +
      '<span>' + esc(coverage) + '</span></div>' +
      (corridor.notes ? '<div class="corridor-gap">' + untranslated(corridor.notes) + '</div>' : '') +
      '</button>';
  }

  function renderCorridors() {
    dom.exploreContent.hidden = true;
    dom.exploreContent.style.display = 'none';
    dom.viewPanel.hidden = false;
    const list = filteredCorridors();
    dom.viewPanel.innerHTML =
      '<div class="corridor-intro"><h2>' + esc(t('corridor.trans_corridors')) + '</h2>' +
      '<p>' + esc(t('corridor.intro')) + '</p></div>' +
      '<div class="corridor-list">' + (list.length
        ? list.map(corridorCard).join('')
        : '<div class="list-empty"><h3>' + esc(t('corridors.no_match')) + '</h3><p>' +
          esc(t('corridors.no_match_body')) + '</p></div>') + '</div>';
  }

  /* ---------- estates view ---------- */

  function ensureEstates() {
    if (estatesState === 'ready' || estatesState === 'loading') return;
    estatesState = 'loading';
    const script = document.createElement('script');
    script.src = (window.ATLAS_BASE || '') + 'data/estates.js';
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

  function ensureCompanies() {
    if (companiesState === 'ready' || companiesState === 'loading') return;
    companiesState = 'loading';
    const script = document.createElement('script');
    script.src = (window.ATLAS_BASE || '') + 'data/companies.js';
    script.onload = function () {
      companies = window.INFRA_COMPANIES || [];
      companiesState = 'ready';
      if (state.view === 'companies') renderAll();
    };
    script.onerror = function () {
      companiesState = 'error';
      if (state.view === 'companies') renderAll();
    };
    document.body.appendChild(script);
  }

  function ensureProgrammes() {
    if (programmesState === 'ready' || programmesState === 'loading') return;
    programmesState = 'loading';
    // Load the eight PKPN first, then the 24 PSN programmes. A missing PKPN
    // file must not block the PSN register.
    const script = document.createElement('script');
    script.src = (window.ATLAS_BASE || '') + 'data/pkpn.js';
    script.onload = function () {
      pkpn = window.INFRA_PKPN || [];
      loadProgrammesPayload();
    };
    script.onerror = function () {
      pkpn = [];
      loadProgrammesPayload();
    };
    document.body.appendChild(script);
  }

  function loadProgrammesPayload() {
    const script = document.createElement('script');
    script.src = (window.ATLAS_BASE || '') + 'data/programmes.js';
    script.onload = function () {
      programmes = window.INFRA_PROGRAMMES || [];
      programmesState = 'ready';
      if (state.view === 'programmes') renderAll();
    };
    script.onerror = function () {
      programmesState = 'error';
      if (state.view === 'programmes') renderAll();
    };
    document.body.appendChild(script);
  }

  function estateTypeLabel(type) {
    return tOr('estate_type.' + type, type);
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
        if (!matchesHaystack(haystack, query)) return false;
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
    const source = estate.source_publisher || t('estates.source_label');
    const coords = fmtCoord(estate.lat) + ', ' + fmtCoord(estate.lon);
    const location = [estate.regency, provinceText(estate.province)].filter(Boolean).join(' · ');
    const area = estate.area_ha ? fmtNum(estate.area_ha) + ' ' + t('estates.ha') : t('estates.area_not_sourced');
    const coordinateNote = estate.coordinate_source === 'unknown'
      ? t('estates.province_centroid')
      : tOr('filter.' + estate.precision, estate.precision);
    return '<div class="estate-row"><button type="button" data-estate="' + esc(estate.id) +
      '" aria-expanded="' + expanded + '"><span><span class="estate-name">' + esc(estate.name) +
      '<span class="type-tag">' + esc(estateTypeLabel(estate.type)) + '</span></span>' +
      '<span class="estate-sub">' + esc(location) + '</span></span>' +
      '<span class="estate-area">' + esc(area) + '<small>' + esc(statusLabel(estate.status)) +
      '</small></span></button>' +
      (expanded ? '<div class="estate-detail">' +
        '<dl><dt>' + esc(t('estates.developer')) + '</dt><dd>' + esc(estate.developer || t('estates.not_sourced')) + '</dd>' +
        '<dt>' + esc(t('estates.sector_focus')) + '</dt><dd>' + esc(estate.sector_focus || t('estates.not_stated')) + '</dd>' +
        '<dt>' + esc(t('estates.legal_basis')) + '</dt><dd>' + esc(estate.legal_basis || t('estates.not_stated')) + '</dd>' +
        '<dt>' + esc(t('estates.established')) + '</dt><dd>' + esc(estate.established_year || t('estates.not_stated')) + '</dd>' +
        '<dt>' + esc(t('estates.website')) + '</dt><dd>' + (estate.website ? '<a href="' + esc(estate.website) + '" target="_blank" rel="noopener">' + esc(estate.website) + '</a>' : esc(t('estates.not_recorded'))) + '</dd>' +
        '<dt>' + esc(t('estates.coordinates')) + '</dt><dd>' + esc(coords) + ' · ' + esc(coordinateNote) + '</dd>' +
        '<dt>' + esc(t('estates.source')) + '</dt><dd>' + esc(source) + (estate.source_url ? ' · <a href="' + esc(estate.source_url) + '" target="_blank" rel="noopener">' + esc(t('estates.open_source')) + '</a>' : '') + '</dd>' +
        '<dt>' + esc(t('estates.verified')) + '</dt><dd>' + esc(fmtDate(estate.last_verified)) + '</dd></dl>' +
        (estate.notes ? '<p class="estate-detail-note">' + untranslated(estate.notes) + '</p>' : '') +
        '</div>' : '') + '</div>';
  }

  function renderEstates() {
    dom.exploreContent.hidden = true;
    dom.exploreContent.style.display = 'none';
    dom.viewPanel.hidden = false;

    if (estatesState === 'loading') {
      dom.viewPanel.innerHTML = '<div class="data-view"><h2>' + esc(t('estates.title')) + '</h2>' +
        '<p class="lede">' + esc(t('result.loading_estates')) + '</p></div>';
      return;
    }
    if (estatesState === 'error') {
      dom.viewPanel.innerHTML = '<div class="data-view"><h2>' + esc(t('estates.title')) + '</h2>' +
        '<p class="notes-callout">' + esc(t('result.estates_error')) + '</p></div>';
      return;
    }
    if (!estates) {
      dom.viewPanel.innerHTML = '<div class="data-view"><h2>' + esc(t('estates.title')) + '</h2>' +
        '<p class="lede">' + esc(t('result.loading_estates')) + '</p></div>';
      ensureEstates();
      return;
    }

    const list = filteredEstates();
    const gapInfo = (stats.estates && stats.estates.gap_dispositions) || {};
    const gapResolved = gapInfo.resolved || 0;
    const gapOpen = (gapInfo['unresolved-no-source'] || 0) + (gapInfo['unresolved-location-conflict'] || 0);
    const gapNotRequired = gapInfo['not-required-for-count'] || 0;
    const typeCounts = { all: estates.length, sez: 0, industrial_estate: 0, both: 0 };
    estates.forEach(function (estate) {
      if (estate.type === 'sez' || estate.type === 'both') typeCounts.sez += 1;
      if (estate.type === 'industrial_estate' || estate.type === 'both') typeCounts.industrial_estate += 1;
      if (estate.type === 'both') typeCounts.both += 1;
    });
    const provinces = Array.from(new Set(estates.map(function (estate) { return estate.province; }))).sort();
    const totalArea = estates.reduce(function (sum, estate) { return sum + (Number(estate.area_ha) || 0); }, 0);
    const types = [
      { key: 'all', label: t('estates.all'), count: typeCounts.all },
      { key: 'sez', label: t('estates.sez'), count: typeCounts.sez },
      { key: 'industrial_estate', label: t('estates.industrial'), count: typeCounts.industrial_estate },
      { key: 'both', label: t('estates.both'), count: typeCounts.both }
    ];

    dom.viewPanel.innerHTML =
      '<div class="estate-tools"><h2>' + esc(t('estates.title')) + '</h2>' +
      '<p>' + esc(t('estates.records', {
        total: fmtNum(estates.length), sez: fmtNum(typeCounts.sez),
        industrial: fmtNum(typeCounts.industrial_estate), both: fmtNum(typeCounts.both)
      })) + '</p>' +
      '<div class="estate-summary">' +
      '<div><div class="k">' + esc(t('estates.zones')) + '</div><div class="v">' + fmtNum(estates.length) + '</div></div>' +
      '<div><div class="k">' + esc(t('estates.total_area')) + '</div><div class="v">' + fmtNum(Math.round(totalArea)) + ' <small>' + esc(t('estates.ha')) + '</small></div></div>' +
      '<div><div class="k">' + esc(t('estates.sezs')) + '</div><div class="v">' + fmtNum(typeCounts.sez) + '</div></div>' +
      '<div><div class="k">' + esc(t('estates.provinces')) + '</div><div class="v">' + fmtNum(provinces.length) + '</div></div>' +
      '</div>' +
      '<div class="chip-row" style="margin-bottom:9px">' + types.map(function (type) {
        return '<button class="chip" data-estate-type="' + esc(type.key) + '" aria-pressed="' +
          (state.estateType === type.key) + '">' + esc(type.label) +
          '<span class="chip-count">' + fmtNum(type.count) + '</span></button>';
      }).join('') + '</div>' +
      '<div class="filter-actions" style="margin-top:0">' +
      '<label class="field" style="flex:1"><span class="sr-only">' + esc(t('filter.province')) + '</span><select id="estate-province">' +
      '<option value="">' + esc(t('estates.any_province')) + '</option>' + provinces.map(function (province) {
        return '<option value="' + esc(province) + '"' + (state.estateProvince === province ? ' selected' : '') +
          '>' + esc(provinceText(province)) + '</option>';
      }).join('') + '</select></label>' +
      '<label class="field" style="flex:1"><span class="sr-only">' + esc(t('sort.estates')) + '</span><select id="estate-sort">' +
      '<option value="name"' + (state.estateSort === 'name' ? ' selected' : '') + '>' + esc(t('estates.name_az')) + '</option>' +
      '<option value="area"' + (state.estateSort === 'area' ? ' selected' : '') + '>' + esc(t('estates.largest_area')) + '</option>' +
      '<option value="province"' + (state.estateSort === 'province' ? ' selected' : '') + '>' + esc(t('estates.provinces')) + '</option>' +
      '</select></label></div>' +
      '<div class="filter-actions" style="margin-top:9px"><span class="corridor-meta">' +
      esc(t('estates.shown', { shown: fmtNum(list.length), total: fmtNum(estates.length) })) +
      '</span><button class="filter-clear" type="button" data-export="estates-csv">' +
      esc(t('estates.download')) + '</button></div></div>' +
      '<div class="estate-list">' + (list.length ? list.map(estateRow).join('') :
        '<div class="list-empty"><h3>' + esc(t('estates.no_match')) + '</h3><p>' + esc(t('estates.no_match_body')) + '</p></div>') + '</div>' +
      '<p class="estate-note">' + esc(t('estates.note', {
        resolved: fmtNum(gapResolved), open: fmtNum(gapOpen), not_required: fmtNum(gapNotRequired)
      })) + '</p>';

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

  /* ---------- filtered exports ---------- */

  function csvCell(value) {
    if (value == null) return '';
    const text = Array.isArray(value) ? JSON.stringify(value) : String(value);
    return /[",\n\r]/.test(text) ? '"' + text.replace(/"/g, '""') + '"' : text;
  }

  function toCsv(rows, fields) {
    return [fields.join(',')].concat(rows.map(function (row) {
      return fields.map(function (field) { return csvCell(row[field]); }).join(',');
    })).join('\r\n') + '\r\n';
  }

  function downloadBlob(filename, content, type) {
    const blob = new Blob([content], { type: type || 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
    toast(t('toast.download_started', { file: filename }));
  }

  const PROJECT_EXPORT_FIELDS = [
    'id', 'name', 'sector', 'subsector', 'status', 'province', 'island', 'route',
    'length_km', 'operational_km', 'construction_km', 'progress_pct',
    'investment_idr_t', 'capacity', 'capacity_unit', 'psn', 'opened_year',
    'opened_date', 'expected_open_year', 'status_as_of', 'verification', 'lat',
    'lon', 'precision', 'operator', 'source_url', 'source_type', 'retrieved_on',
    'last_verified', 'freshness_state', 'notes'
  ];

  function exportFilteredProjects(format) {
    const list = sortProjects(filteredProjects());
    if (!list.length) {
      toast(t('toast.no_projects'));
      return;
    }
    if (format === 'geojson') {
      const features = list.map(function (project) {
        const properties = Object.assign({}, project);
        delete properties.lat;
        delete properties.lon;
        return {
          type: 'Feature',
          geometry: { type: 'Point', coordinates: [Number(project.lon), Number(project.lat)] },
          properties: properties
        };
      });
      downloadBlob(
        'infra-id-projects-filtered.geojson',
        JSON.stringify({ type: 'FeatureCollection', features: features }, null, 2) + '\n',
        'application/geo+json'
      );
      return;
    }
    downloadBlob(
      'infra-id-projects-filtered.csv',
      toCsv(list, PROJECT_EXPORT_FIELDS),
      'text/csv;charset=utf-8'
    );
  }

  function exportFilteredEstates() {
    if (!estates) {
      ensureEstates();
      toast(t('toast.estates_loading'));
      return;
    }
    const list = filteredEstates();
    if (!list.length) {
      toast(t('toast.no_estates'));
      return;
    }
    const fields = Object.keys(list[0]);
    downloadBlob(
      'infra-id-estates-filtered.csv',
      toCsv(list, fields),
      'text/csv;charset=utf-8'
    );
  }

  function exportFilteredCompanies() {
    if (!companies) {
      ensureCompanies();
      toast(t('toast.companies_loading'));
      return;
    }
    const list = filteredCompanies();
    if (!list.length) {
      toast(t('toast.no_companies'));
      return;
    }
    const fields = [
      'id', 'name', 'short_name', 'org_type', 'country_code', 'parent_id',
      'website', 'project_count', 'role_count', 'notes',
    ];
    downloadBlob(
      'infra-id-companies-filtered.csv',
      toCsv(list, fields),
      'text/csv;charset=utf-8'
    );
  }

  function handleExport(kind) {
    if (kind === 'projects-csv') exportFilteredProjects('csv');
    else if (kind === 'projects-geojson') exportFilteredProjects('geojson');
    else if (kind === 'estates-csv') exportFilteredEstates();
    else if (kind === 'companies-csv') exportFilteredCompanies();
  }

  /* ---------- programme view ---------- */

  function programmeThemeLabel(theme) {
    return theme ? tOr('theme.' + theme, theme) : t('theme.other');
  }

  function programmeThemeColor(theme) {
    return (PROGRAMME_THEMES[theme] && PROGRAMME_THEMES[theme].color) || '#475569';
  }

  function pkpnLabel(id) {
    if (!id) return t('pkpn.none');
    return tOr('pkpn.' + id.replace(/^pkpn-/, ''), t('pkpn.none'));
  }

  function programmeRoleLabel(role) {
    return tOr('programme_role.' + role, role);
  }

  function filteredProgrammes() {
    if (!programmes) return [];
    const query = state.q.toLowerCase().trim();
    return programmes.filter(function (programme) {
      if (state.programmeTheme !== 'all' && programme.theme !== state.programmeTheme) return false;
      if (!query) return true;
      const haystack = [
        programme.name_en, programme.name_id, programme.summary_en, programme.summary_id,
        programme.lead_org_name, programme.lead_org_short, programme.pkpn_id,
        programmeThemeLabel(programme.theme)
      ].join(' ').toLowerCase();
      return matchesHaystack(haystack, query);
    });
  }

  function programmeCard(programme) {
    const theme = programmeThemeColor(programme.theme);
    const lead = programme.lead_org_short || programme.lead_org_name || t('programmes.lead_missing');
    const projects = programme.projects || [];
    const projectList = projects.length
      ? '<div class="programme-projects"><div class="programme-sub">' + esc(t('programmes.linked_atlas')) + '</div><ul>' +
        projects.map(function (project) {
          return '<li><a href="#/project/' + esc(project.id) + '">' + esc(projectName(project)) + '</a>' +
            '<span>' + esc(statusLabel(project.status)) + ' · ' + esc(programmeRoleLabel(project.role)) + '</span></li>';
        }).join('') + '</ul></div>'
      : '<p class="programme-empty">' + esc(t('programmes.no_projects')) + '</p>';
    const primaryName = programmeName(programme);
    const secondaryName = I18N.locale === 'id' ? programme.name_en : programme.name_id;
    const primarySummary = programmeField(programme, 'summary') ||
      (I18N.locale === 'id' ? programme.summary_id : programme.summary_en);
    const secondarySummary = I18N.locale === 'id' ? programme.summary_en : programme.summary_id;
    const primaryLang = I18N.locale === 'id' ? 'id' : 'en';
    const secondaryLang = I18N.locale === 'id' ? 'en' : 'id';
    const primaryLabel = primaryLang.toUpperCase();
    const secondaryLabel = secondaryLang.toUpperCase();
    const target = programmeField(programme, 'target_summary') ||
      (I18N.locale === 'id' ? programme.target_summary_id : programme.target_summary_en);
    return '<article class="programme-card" style="--theme-color:' + esc(theme) + '">' +
      '<div class="programme-top"><span class="programme-no">' + esc(t('programmes.psn_no', { number: programme.psn_no })) + '</span>' +
      '<span class="programme-theme">' + esc(programmeThemeLabel(programme.theme)) + '</span></div>' +
      '<h3>' + esc(primaryName) + '</h3>' +
      (secondaryName && secondaryName !== primaryName
        ? '<p class="programme-id" lang="' + secondaryLang + '">' + esc(secondaryName) + '</p>'
        : '') +
      (primarySummary
        ? '<p class="programme-summary" lang="' + primaryLang + '"><span class="programme-lang">' + primaryLabel + '</span>' + esc(primarySummary) + '</p>'
        : '<p class="programme-summary programme-summary-missing"><span class="programme-lang">' + primaryLabel + '</span>' + esc(t('programmes.summary_missing')) + '</p>') +
      (secondarySummary && secondarySummary !== primarySummary
        ? '<p class="programme-summary programme-summary-id" lang="' + secondaryLang + '"><span class="programme-lang">' + secondaryLabel + '</span>' + esc(secondarySummary) + '</p>'
        : '') +
      '<dl class="programme-meta">' +
      '<div><dt>' + esc(t('programmes.lead')) + '</dt><dd>' + esc(lead) + '</dd></div>' +
      '<div><dt>' + esc(t('programmes.pkpn')) + '</dt><dd>' + esc(pkpnLabel(programme.pkpn_id)) + '</dd></div>' +
      '<div><dt>' + esc(t('programmes.target')) + '</dt><dd>' + esc(target || t('programmes.not_published')) + '</dd></div>' +
      '</dl>' +
      ((programme.indicators && programme.indicators.length)
        ? '<div class="programme-indicators"><div class="programme-sub">' +
          esc(t('programmes.target_current')) + '</div><ul>' +
          programme.indicators.map(function (indicator) {
            const info = indicatorSummary(indicator);
            const targetText = info.target ? ' · ' + t('indicator.target') + ' ' + info.target : '';
            const current = info.hasValue
              ? t('indicator.current') + ' ' + info.current
              : t('indicator.no_value');
            return '<li><b>' + esc(info.name) + '</b><span>' + esc(current) + esc(targetText) +
              (info.asOf ? ' · ' + esc(info.asOf) : '') + '</span></li>';
          }).join('') + '</ul></div>'
        : '') +
      projectList +
      (programme.source_url
        ? '<a class="programme-source" href="' + esc(programme.source_url) + '" target="_blank" rel="noopener">' +
          esc(programme.source_title || t('programmes.official_source')) + ' ↗</a>'
        : '') +
      '</article>';
  }

  function pkpnCard(item) {
    const name = localName(item);
    const secondary = I18N.locale === 'id' ? item.name_en : item.name_id;
    const secondaryLang = I18N.locale === 'id' ? 'en' : 'id';
    const summary = I18N.locale === 'id' ? item.summary_id : item.summary_en;
    const target = I18N.locale === 'id' ? item.target_summary_id : item.target_summary_en;
    const budget = item.budget_idr_t
      ? fmtInvestment(item.budget_idr_t)
      : t('programmes.not_published');
    const indicators = (item.indicators || []).map(function (indicator) {
      const info = indicatorSummary(indicator);
      const targetText = info.target ? ' · ' + t('indicator.target') + ' ' + info.target : '';
      const current = info.hasValue
        ? t('indicator.current') + ' ' + info.current
        : t('indicator.no_value');
      return '<li><b>' + esc(info.name) + '</b><span>' + esc(current) + esc(targetText) +
        (info.asOf ? ' · ' + esc(info.asOf) : '') + '</span></li>';
    }).join('');
    return '<article class="pkpn-card" style="--theme-color:' + esc(programmeThemeColor(item.theme)) + '">' +
      '<div class="programme-top"><span class="programme-no">PKPN</span>' +
      '<span class="programme-theme">' + esc(programmeThemeLabel(item.theme)) + '</span></div>' +
      '<h3>' + esc(name) + '</h3>' +
      (secondary && secondary !== name
        ? '<p class="programme-id" lang="' + secondaryLang + '">' + esc(secondary) + '</p>'
        : '') +
      '<p class="programme-summary">' + esc(summary) + '</p>' +
      '<dl class="programme-meta">' +
      '<div><dt>' + esc(t('programmes.pkpn_target')) + '</dt><dd>' +
      esc(target || t('programmes.pkpn_no_target')) + '</dd></div>' +
      '<div><dt>' + esc(t('programmes.pkpn_budget')) + '</dt><dd>' + esc(budget) + '</dd></div>' +
      '</dl>' +
      (indicators
        ? '<div class="programme-indicators"><div class="programme-sub">' +
          esc(t('programmes.target_current')) + '</div><ul>' + indicators + '</ul></div>'
        : '') +
      (item.source_url
        ? '<a class="programme-source" href="' + esc(item.source_url) + '" target="_blank" rel="noopener">' +
          esc(item.source_title || t('programmes.official_source')) + ' ↗</a>'
        : '') +
      '</article>';
  }

  function renderProgrammes() {
    dom.exploreContent.hidden = true;
    dom.exploreContent.style.display = 'none';
    dom.viewPanel.hidden = false;

    if (programmesState === 'loading') {
      dom.viewPanel.innerHTML = '<div class="data-view"><h2>' + esc(t('programmes.title')) + '</h2>' +
        '<p class="lede">' + esc(t('result.loading_programmes')) + '</p></div>';
      return;
    }
    if (programmesState === 'error') {
      dom.viewPanel.innerHTML = '<div class="data-view"><h2>' + esc(t('programmes.title')) + '</h2>' +
        '<p class="notes-callout">' + esc(t('result.programmes_error')) + '</p></div>';
      return;
    }
    if (!programmes) {
      dom.viewPanel.innerHTML = '<div class="data-view"><h2>' + esc(t('programmes.title')) + '</h2>' +
        '<p class="lede">' + esc(t('result.loading_programmes')) + '</p></div>';
      ensureProgrammes();
      return;
    }

    const list = filteredProgrammes();
    const themeCounts = { all: programmes.length };
    programmes.forEach(function (programme) {
      themeCounts[programme.theme] = (themeCounts[programme.theme] || 0) + 1;
    });
    const statsProgrammes = stats.programmes || {};
    const themes = [{ key: 'all', label: t('programmes.all'), count: themeCounts.all }].concat(
      PROGRAMME_THEME_ORDER.filter(function (theme) { return themeCounts[theme]; })
        .map(function (theme) {
          return { key: theme, label: programmeThemeLabel(theme), count: themeCounts[theme] };
        })
    );

    dom.viewPanel.innerHTML = '<div class="programme-view">' +
      '<header class="programme-hero">' +
      '<p class="kicker">' + esc(t('programmes.register_kicker')) + '</p>' +
      '<h2>' + esc(t('programmes.title')) + '</h2>' +
      '<p class="lede">' + esc(t('programmes.register_lede')) + '</p>' +
      '</header>' +
      (pkpn && pkpn.length
        ? '<section class="pkpn-section"><div class="psn-head"><p class="kicker">' +
          esc(t('programmes.pkpn_kicker')) + '</p><h3>' + esc(t('programmes.pkpn_title')) +
          '</h3><p class="lede">' + esc(t('programmes.pkpn_lede')) + '</p></div>' +
          '<div class="pkpn-grid">' + pkpn.map(pkpnCard).join('') + '</div></section>'
        : '') +
      '<div class="psn-head"><p class="kicker">' + esc(t('programmes.kicker')) +
      '</p><h3>' + esc(t('programmes.psn_title')) + '</h3>' +
      '<p class="lede">' + esc(t('programmes.lede')) + '</p></div>' +
      '<div class="programme-stats">' +
      '<div><span class="k">' + esc(t('programmes.programmes')) + '</span><strong>' + fmtNum(statsProgrammes.total || programmes.length) + '</strong><small>' + esc(t('programmes.active')) + '</small></div>' +
      '<div><span class="k">' + esc(t('programmes.with_lead')) + '</span><strong>' + fmtNum(statsProgrammes.with_lead || 0) + '</strong><small>' + esc(t('programmes.of', { total: fmtNum(programmes.length) })) + '</small></div>' +
      '<div><span class="k">' + esc(t('programmes.linked_projects')) + '</span><strong>' + fmtNum(statsProgrammes.with_projects || 0) + '</strong><small>' + esc(t('programmes.programmes_lower')) + '</small></div>' +
      '<div><span class="k">' + esc(t('programmes.atomic_claims')) + '</span><strong>' + fmtNum(statsProgrammes.claims || 0) + '</strong><small>' + esc(t('programmes.programme_facts')) + '</small></div>' +
      '<div><span class="k">' + esc(t('programmes.targets_published')) + '</span><strong>' + fmtNum(statsProgrammes.with_target || 0) + '</strong><small>' + esc(t('programmes.of', { total: fmtNum(programmes.length) })) + '</small></div>' +
      '</div>' +
      '<div class="programme-toolbar">' +
      '<span class="programme-count">' + esc(t('programmes.shown', { shown: fmtNum(list.length), total: fmtNum(programmes.length) })) + '</span>' +
      '</div>' +
      '<div class="chip-row programme-chips">' + themes.map(function (theme) {
        return '<button class="chip" data-programme-theme="' + esc(theme.key) + '" aria-pressed="' +
          String(state.programmeTheme === theme.key) + '">' + esc(theme.label) +
          '<span class="chip-count">' + fmtNum(theme.count) + '</span></button>';
      }).join('') + '</div>' +
      (list.length
        ? '<div class="programme-grid">' + list.map(programmeCard).join('') + '</div>'
        : '<p class="notes-callout">' + esc(t('programmes.no_match')) + '</p>') +
      '</div>';

    dom.viewPanel.querySelectorAll('[data-programme-theme]').forEach(function (chip) {
      chip.addEventListener('click', function () {
        state.programmeTheme = chip.getAttribute('data-programme-theme');
        renderAll();
      });
    });
  }

  /* ---------- companies view ---------- */

  function orgTypeLabel(type) {
    return tOr('org_type.' + type, type);
  }

  function roleLabel(role) {
    return tOr('role.' + role, role);
  }

  function filteredCompanies() {
    if (!companies) return [];
    const query = state.q.toLowerCase().trim();
    return companies.filter(function (company) {
      if (state.companyType !== 'all' && company.org_type !== state.companyType) return false;
      if (!query) return true;
      const entry = searchCompanies.get(company.id);
      const haystack = (entry ? entry.text :
        [company.name, company.short_name, company.org_type, company.country_code]
          .join(' ')).toLowerCase();
      return matchesHaystack(haystack, query);
    }).sort(function (a, b) {
      if (state.companySort === 'projects') {
        return (b.project_count || 0) - (a.project_count || 0) || a.name.localeCompare(b.name);
      }
      return a.name.localeCompare(b.name);
    });
  }

  function companyRoles(company) {
    const roles = company.roles || [];
    if (!roles.length) {
      return '<p class="programme-empty">' + esc(t('companies.no_roles')) + '</p>';
    }
    return '<ul class="company-role-list">' + roles.map(function (role) {
      const years = role.start_year || role.end_year
        ? t('companies.years', {
          start: role.start_year || '—', end: role.end_year || '—'
        })
        : '';
      const meta = [statusLabel(role.status), sectorLabel(role.sector), roleLabel(role.role)]
        .filter(Boolean).join(' · ');
      return '<li><a href="#/project/' + esc(role.project_id) + '">' +
        esc(projectName({ id: role.project_id, name: role.project_name })) + '</a>' +
        '<span>' + esc(meta) +
        (role.share_pct ? ' · ' + esc(t('companies.share')) + ' ' + fmtNum(role.share_pct) + '%' : '') +
        (years ? ' · ' + esc(years) : '') + '</span>' +
        (role.source_url ? '<a class="company-source" href="' + esc(role.source_url) +
          '" target="_blank" rel="noopener">' + esc(t('companies.source')) + ' ↗</a>' : '') +
        '</li>';
    }).join('') + '</ul>';
  }

  function companyRow(company) {
    const expanded = state.expandedCompany === company.id;
    const roles = company.roles || [];
    const projectCount = company.project_count || 0;
    const location = [company.country_code,
      projectCount === 1 ? t('companies.project_count_one') :
        t('companies.project_count', { count: fmtNum(projectCount) })
    ].filter(Boolean).join(' · ');
    return '<div class="company-row"><button type="button" data-company="' + esc(company.id) +
      '" aria-expanded="' + expanded + '"><span><span class="company-name">' + esc(company.name) +
      (company.short_name ? ' <span class="company-short">' + esc(company.short_name) + '</span>' : '') +
      '<span class="type-tag">' + esc(orgTypeLabel(company.org_type)) + '</span></span>' +
      '<span class="estate-sub">' + esc(location) + '</span></span>' +
      '<span class="company-count">' +
      esc(roles.length === 1 ? t('companies.role_count_one') :
        t('companies.role_count', { count: fmtNum(roles.length) })) +
      '</span></button>' +
      (expanded ? '<div class="company-detail">' +
        '<dl><dt>' + esc(t('companies.website')) + '</dt><dd>' +
        (company.website ? '<a href="' + esc(company.website) + '" target="_blank" rel="noopener">' +
          esc(company.website) + '</a>' : esc(t('estates.not_recorded'))) + '</dd>' +
        (company.notes ? '<dt>' + esc(t('companies.notes')) + '</dt><dd>' + untranslated(company.notes) + '</dd>' : '') +
        '</dl>' +
        '<div class="company-roles-title">' + esc(t('companies.roles_title')) + '</div>' +
        companyRoles(company) + '</div>' : '') + '</div>';
  }

  function renderCompanies() {
    dom.exploreContent.hidden = true;
    dom.exploreContent.style.display = 'none';
    dom.viewPanel.hidden = false;

    if (companiesState === 'loading') {
      dom.viewPanel.innerHTML = '<div class="data-view"><h2>' + esc(t('companies.title')) + '</h2>' +
        '<p class="lede">' + esc(t('result.loading')) + '</p></div>';
      return;
    }
    if (companiesState === 'error') {
      dom.viewPanel.innerHTML = '<div class="data-view"><h2>' + esc(t('companies.title')) + '</h2>' +
        '<p class="notes-callout">' + esc(t('result.programmes_error')) + '</p></div>';
      return;
    }
    if (!companies) {
      dom.viewPanel.innerHTML = '<div class="data-view"><h2>' + esc(t('companies.title')) + '</h2>' +
        '<p class="lede">' + esc(t('result.loading')) + '</p></div>';
      ensureCompanies();
      return;
    }

    const list = filteredCompanies();
    const orgStats = stats.organizations || {};
    const typeCounts = { all: companies.length };
    companies.forEach(function (company) {
      typeCounts[company.org_type] = (typeCounts[company.org_type] || 0) + 1;
    });
    const types = ['all', 'government', 'soe', 'private', 'consortium'].filter(function (type) {
      return type === 'all' || typeCounts[type];
    });
    const countries = Object.keys(orgStats.countries || {}).length;

    dom.viewPanel.innerHTML = '<div class="estate-tools"><h2>' + esc(t('companies.title')) + '</h2>' +
      '<p>' + esc(t('companies.lede')) + '</p>' +
      '<div class="estate-summary">' +
      '<div><div class="k">' + esc(t('companies.organisations')) + '</div><div class="v">' +
      fmtNum(orgStats.total || companies.length) + '</div></div>' +
      '<div><div class="k">' + esc(t('companies.with_links')) + '</div><div class="v">' +
      fmtNum(orgStats.with_links || 0) + '</div></div>' +
      '<div><div class="k">' + esc(t('companies.roles')) + '</div><div class="v">' +
      fmtNum(orgStats.links || 0) + '</div></div>' +
      '<div><div class="k">' + esc(t('companies.countries')) + '</div><div class="v">' +
      fmtNum(countries) + '</div></div>' +
      '</div>' +
      '<div class="chip-row" style="margin-bottom:9px">' + types.map(function (type) {
        return '<button class="chip" data-company-type="' + esc(type) + '" aria-pressed="' +
          (state.companyType === type) + '">' +
          esc(type === 'all' ? t('companies.all') : orgTypeLabel(type)) +
          '<span class="chip-count">' + fmtNum(typeCounts[type] || 0) + '</span></button>';
      }).join('') + '</div>' +
      '<div class="filter-actions" style="margin-top:0">' +
      '<label class="field" style="flex:1"><span class="sr-only">' + esc(t('companies.sort')) +
      '</span><select id="company-sort">' +
      '<option value="name"' + (state.companySort === 'name' ? ' selected' : '') + '>' +
      esc(t('companies.sort_name')) + '</option>' +
      '<option value="projects"' + (state.companySort === 'projects' ? ' selected' : '') + '>' +
      esc(t('companies.sort_projects')) + '</option>' +
      '</select></label></div>' +
      '<div class="filter-actions" style="margin-top:9px"><span class="corridor-meta">' +
      esc(t('companies.shown', { shown: fmtNum(list.length), total: fmtNum(companies.length) })) +
      '</span><button class="filter-clear" type="button" data-export="companies-csv">' +
      esc(t('companies.download')) + '</button></div></div>' +
      '<div class="estate-list">' + (list.length ? list.map(companyRow).join('') :
        '<div class="list-empty"><h3>' + esc(t('companies.no_match')) + '</h3><p>' +
        esc(t('companies.no_match_body')) + '</p></div>') + '</div>';

    dom.viewPanel.querySelectorAll('[data-company-type]').forEach(function (chip) {
      chip.addEventListener('click', function () {
        state.companyType = chip.getAttribute('data-company-type');
        commit(false);
      });
    });
    dom.viewPanel.querySelectorAll('[data-company]').forEach(function (row) {
      row.addEventListener('click', function () {
        const id = row.getAttribute('data-company');
        state.expandedCompany = state.expandedCompany === id ? null : id;
        renderCompanies();
      });
    });
    const sortSelect = $('company-sort');
    if (sortSelect) sortSelect.addEventListener('change', function () {
      state.companySort = sortSelect.value;
      commit(false);
    });
  }

  /* ---------- data view ---------- */

  function downloadUrl(file) {
    return (window.ATLAS_BASE || '') + file;
  }

  function coverageLabel(row) {
    return tOr('coverage.' + row.layer, row.label);
  }

  function coverageHeader(key, label) {
    const active = state.coverageSort.key === key;
    const direction = active ? state.coverageSort.dir : 0;
    const ariaSort = active ? (direction > 0 ? 'ascending' : 'descending') : 'none';
    const indicator = active
      ? '<span class="sort-indicator" aria-hidden="true">' + (direction > 0 ? '▲' : '▼') + '</span>'
      : '';
    return '<th class="' + (key === 'layer' ? '' : 'num') + '" aria-sort="' + ariaSort + '">' +
      '<button type="button" class="sort-button" data-coverage-sort="' + key + '">' +
      esc(label) + indicator + '</button></th>';
  }

  function coverageRows() {
    const source = stats.coverage || [];
    const sorted = state.coverageSort.key ? source.slice().sort(function (a, b) {
      const key = state.coverageSort.key;
      const factor = state.coverageSort.dir;
      if (key === 'layer') {
        return coverageLabel(a).localeCompare(
          coverageLabel(b), I18N.locale === 'id' ? 'id' : 'en'
        ) * factor;
      }
      const aValue = key === 'gap' && a.status === 'met' ? 0 : Number(a[key] || 0);
      const bValue = key === 'gap' && b.status === 'met' ? 0 : Number(b[key] || 0);
      if (aValue !== bValue) return (aValue - bValue) * factor;
      return coverageLabel(a).localeCompare(
        coverageLabel(b), I18N.locale === 'id' ? 'id' : 'en'
      );
    }) : source;
    const rows = sorted.map(function (row) {
      return '<tr><td class="layer">' + esc(coverageLabel(row)) +
        '<br><span style="color:var(--muted);font-size:9px">' + esc(row.reference_set) + '</span></td>' +
        '<td class="num">' + fmtNum(row.current) + '</td>' +
        '<td class="num">' + fmtNum(row.target) + '</td>' +
        '<td class="num ' + (row.status === 'met' ? 'ok' : 'gap') + '">' +
        (row.status === 'met' ? esc(t('data.met')) : (row.gap ? '+' + fmtNum(row.gap) : '—')) + '</td></tr>';
    }).join('');
    return '<table class="coverage-table"><thead><tr>' +
      coverageHeader('layer', t('data.layer')) +
      coverageHeader('current', t('data.now')) +
      coverageHeader('target', t('data.target')) +
      coverageHeader('gap', t('data.gap')) +
      '</tr></thead><tbody>' + rows + '</tbody></table>';
  }

  function stackBar(counts) {
    const order = [
      ['fresh', 'var(--operating)'],
      ['due_soon', 'var(--accent)'],
      ['stale', 'var(--stalled)'],
      ['unknown', 'var(--muted)']
    ];
    const total = order.reduce(function (sum, entry) { return sum + (counts[entry[0]] || 0); }, 0);
    if (!total) return '<p class="basis">—</p>';
    const segments = order.map(function (entry) {
      const count = counts[entry[0]] || 0;
      if (!count) return '';
      return '<span style="width:' + ((count / total) * 100) + '%;background:' + entry[1] +
        '" title="' + esc(t('freshness.' + entry[0])) + ': ' + fmtNum(count) + '"></span>';
    }).join('');
    const legend = order.filter(function (entry) { return counts[entry[0]]; }).map(function (entry) {
      return '<span class="chart-legend-item"><i style="background:' + entry[1] + '"></i>' +
        esc(entry[0] === 'fresh' ? t('freshness.fresh_short') : t('freshness.' + entry[0])) +
        ' ' + fmtNum(counts[entry[0]]) + '</span>';
    }).join('');
    return '<div class="status-stack" role="img" aria-label="' +
      esc(t('data.chart_aria', { title: t('data.freshness_chart'), count: fmtNum(total) })) +
      '">' + segments + '</div><div class="chart-legend">' + legend + '</div>';
  }

  function chartsSection() {
    const projectStats = stats.projects || {};
    const sectorCounts = projectStats.by_sector || {};
    const statusCounts = projectStats.by_status || {};
    const freshness = stats.freshness || {};
    const freshnessCounts = freshness.counts || {};
    const sectorRows = SECTOR_ORDER
      .filter(function (sector) { return sectorCounts[sector]; })
      .sort(function (a, b) { return (sectorCounts[b] || 0) - (sectorCounts[a] || 0); });
    const sectorMax = sectorRows.reduce(function (best, sector) {
      return Math.max(best, sectorCounts[sector] || 0);
    }, 1);
    const sectorTotal = sectorRows.reduce(function (sum, sector) {
      return sum + (sectorCounts[sector] || 0);
    }, 0);
    const statusTotal = STATUS_ORDER.reduce(function (sum, status) {
      return sum + (statusCounts[status] || 0);
    }, 0);
    const statusSegments = STATUS_ORDER.map(function (status) {
      const count = statusCounts[status] || 0;
      if (!count) return '';
      return '<span style="width:' + ((count / Math.max(statusTotal, 1)) * 100) +
        '%;background:' + esc((STATUS[status] && STATUS[status].color) || '#667085') +
        '" title="' + esc(statusLabel(status)) + ': ' + fmtNum(count) + '"></span>';
    }).join('');
    const statusLegend = STATUS_ORDER.filter(function (status) {
      return statusCounts[status];
    }).map(function (status) {
      return '<span class="chart-legend-item"><i style="background:' +
        esc((STATUS[status] && STATUS[status].color) || '#667085') + '"></i>' +
        esc(statusLabel(status)) + ' ' + fmtNum(statusCounts[status]) + '</span>';
    }).join('');

    return '<section class="data-section"><h3>' + esc(t('data.charts')) + '</h3>' +
      '<div class="chart-grid">' +
      '<div class="chart" role="group" aria-label="' +
      esc(t('data.chart_aria', { title: t('data.sector_chart'), count: fmtNum(sectorTotal) })) + '">' +
      '<div class="chart-title">' + esc(t('data.sector_chart')) + '</div>' +
      sectorRows.map(function (sector) {
        const count = sectorCounts[sector] || 0;
        return '<div class="bar-row"><span class="bar-label">' + esc(sectorLabel(sector, true)) +
          '</span><span class="bar-track"><span class="bar-fill" style="width:' +
          Math.max(2, (count / sectorMax) * 100) + '%"></span></span><span class="bar-value">' +
          fmtNum(count) + '</span></div>';
      }).join('') + '</div>' +
      '<div class="chart" role="group" aria-label="' +
      esc(t('data.chart_aria', { title: t('data.status_chart'), count: fmtNum(statusTotal) })) + '">' +
      '<div class="chart-title">' + esc(t('data.status_chart')) + '</div>' +
      '<div class="status-stack" role="img" aria-label="' +
      esc(t('data.chart_aria', { title: t('data.status_chart'), count: fmtNum(statusTotal) })) +
      '">' + statusSegments + '</div><div class="chart-legend">' + statusLegend + '</div>' +
      '<div class="chart-title" style="margin-top:16px">' + esc(t('data.freshness_chart')) + '</div>' +
      '<div class="chart-sub">' + esc(t('data.projects')) + '</div>' +
      stackBar(freshnessCounts.project || {}) +
      '<div class="chart-sub">' + esc(t('data.estates_label')) + '</div>' +
      stackBar(freshnessCounts.estate || {}) + '</div>' +
      '</div></section>';
  }

  function sourceRegister() {
    const sources = stats.sources || [];
    if (!sources.length) return '<p>' + esc(t('data.source_missing')) + '</p>';
    const counts = {};
    sources.forEach(function (source) {
      counts[source.source_type] = (counts[source.source_type] || 0) + 1;
    });
    const types = Object.keys(counts).sort().map(function (type) {
      return fmtNum(counts[type]) + ' ' + esc(tOr('data.source_type.' + type, type));
    }).join(' · ');
    return '<p class="src-meta">' + esc(t('data.source_note', {
      count: fmtNum(sources.length), types: types
    })) + '</p>' +
      '<ul class="source-register">' + sources.map(function (source) {
      return '<li><div class="src-title">' + esc(source.title) + '</div>' +
        '<div class="src-meta">' + esc(source.publisher) + ' · ' + esc(tOr('data.source_type.' + source.source_type, source.source_type)) +
        ' · ' + esc(t('data.retrieved', { date: fmtDate(source.retrieved_on) })) +
        (source.archive_path ? ' · ' + esc(t('data.snapshot')) : '') + '</div>' +
        (source.url ? '<a href="' + esc(source.url) + '" target="_blank" rel="noopener">' + esc(t('action.open_source')) + '</a>' : '') +
        '</li>';
    }).join('') + '</ul>';
  }

  function downloadList() {
    const downloads = stats.downloads || [];
    const projectCount = filteredProjects().length;
    const estateCount = estates ? filteredEstates().length : null;
    const icon = '<svg width="13" height="13" aria-hidden="true"><use href="#i-download"></use></svg>';
    let html = '<div class="download-list">' +
      '<button class="download download-primary" type="button" data-export="projects-csv">' +
      '<span>' + esc(t('data.filtered_view')) + ' <small>' +
      esc(t('data.filtered_projects', { count: fmtNum(projectCount), total: fmtNum(projects.length) })) +
      '</small></span>' + icon + '</button>' +
      '<button class="download" type="button" data-export="projects-geojson">' +
      '<span>' + esc(t('data.filtered_view')) + ' <small>' +
      esc(t('data.filtered_points', { count: fmtNum(projectCount) })) +
      '</small></span>' + icon + '</button>';
    if (estateCount !== null) {
      html += '<button class="download" type="button" data-export="estates-csv">' +
        '<span>' + esc(t('data.filtered_view')) + ' <small>' +
        esc(t('data.filtered_estates', { count: fmtNum(estateCount), total: fmtNum(estates.length) })) +
        '</small></span>' + icon + '</button>';
    }
    if (companies) {
      const companyCount = filteredCompanies().length;
      html += '<button class="download" type="button" data-export="companies-csv">' +
        '<span>' + esc(t('data.filtered_view')) + ' <small>' +
        esc(t('data.filtered_companies', { count: fmtNum(companyCount), total: fmtNum(companies.length) })) +
        '</small></span>' + icon + '</button>';
    }
    html += downloads.map(function (item) {
      const label = item.key ? tOr('download.' + item.key, item.label) : item.label;
      return '<a class="download" href="' + esc(downloadUrl(item.file)) + '" download>' +
        '<span>' + esc(label) + ' <small>' + esc(item.meta) + '</small></span>' +
        icon + '</a>';
    }).join('') + '</div>';
    return html;
  }

  function claimsSection() {
    const claims = stats.claims || {};
    const missing = claims.missing || {};
    const missingKeys = Object.keys(missing);
    const gaps = missingKeys.map(function (key) {
      return esc(key.replace(/_/g, ' ')) + ' (' + fmtNum(missing[key]) + ')';
    }).join(', ');
    return '<section class="data-section"><h3>' + esc(t('data.claims_coverage')) + '</h3>' +
      '<div class="data-stats">' +
      '<div class="data-stat"><div class="k">' + esc(t('data.fully_claimed')) + '</div><div class="v">' +
      fmtNum(claims.projects_fully_claimed || 0) + ' / ' + fmtNum(claims.projects_total || 0) +
      ' <small>' + esc(t('data.projects')) + '</small></div></div>' +
      '<div class="data-stat"><div class="k">' + esc(t('data.atomic_claims')) + '</div><div class="v">' +
      fmtNum(claims.total || 0) + ' <small>' + esc(t('data.rows')) + '</small></div></div>' +
      '<div class="data-stat"><div class="k">' + esc(t('data.programme_claims')) + '</div><div class="v">' +
      fmtNum((stats.programmes && stats.programmes.claims) || 0) + ' <small>' + esc(t('data.rows')) + '</small></div></div></div>' +
      '<p>' + esc(t('data.claims_note')) + ' ' +
      (missingKeys.length ? esc(t('data.claim_gaps', { gaps: gaps })) : esc(t('data.no_claim_gaps'))) +
      ' ' + esc(t('data.investments_note')) + '</p>' +
      '</section>';
  }
  function freshnessSection() {
    const freshness = stats.freshness || {};
    const counts = freshness.counts || {};
    const projects = counts.project || {};
    const estates = counts.estate || {};
    const attention = freshness.attention || [];
    let html = '<section class="data-section"><h3>' + esc(t('data.freshness')) + '</h3>' +
      '<div class="data-stats">' +
      '<div class="data-stat"><div class="k">' + esc(t('data.projects_fresh')) + '</div><div class="v">' +
      fmtNum(projects.fresh || 0) + ' / ' + fmtNum((projects.fresh || 0) + (projects.due_soon || 0) + (projects.stale || 0) + (projects.unknown || 0)) +
      ' <small>' + esc(t('data.rows')) + '</small></div></div>' +
      '<div class="data-stat"><div class="k">' + esc(t('data.estates_fresh')) + '</div><div class="v">' +
      fmtNum(estates.fresh || 0) + ' / ' + fmtNum((estates.fresh || 0) + (estates.due_soon || 0) + (estates.stale || 0) + (estates.unknown || 0)) +
      ' <small>' + esc(t('data.rows')) + '</small></div></div></div>' +
      '<p>' + esc(t('data.freshness_note', {
        as_of: fmtDate(freshness.as_of), next_due: fmtDate(freshness.next_due)
      })) + '</p>';
    if (attention.length) {
      html += '<ul class="gap-list">' + attention.slice(0, 12).map(function (row) {
        return '<li><b>' + esc(freshnessLabel(row.state)) + '</b> · ' + esc(row.name) +
          ' (' + esc(row.entity_type) + ', ' + esc(t('drawer.verified', { date: fmtDate(row.last_verified) })) + ')</li>';
      }).join('') + '</ul>';
    } else {
      html += '<p class="src-meta">' + esc(t('data.no_stale')) + '</p>';
    }
    html += '</section>';
    return html;
  }

  function conflictsSection() {
    const conflicts = stats.conflicts || {};
    const rows = conflicts.rows || [];
    if (!rows.length) return '<section class="data-section"><h3>' + esc(t('data.conflict_register')) + '</h3><p>' + esc(t('data.no_conflicts')) + '</p></section>';
    return '<section class="data-section"><h3>' + esc(t('data.conflict_register')) + '</h3>' +
      '<div class="data-stats">' +
      '<div class="data-stat"><div class="k">' + esc(t('data.open')) + '</div><div class="v">' + fmtNum(conflicts.open || 0) + '</div></div>' +
      '<div class="data-stat"><div class="k">' + esc(t('data.resolved')) + '</div><div class="v">' + fmtNum(conflicts.resolved || 0) + '</div></div></div>' +
      '<p>' + esc(t('data.conflict_note')) + '</p>' +
      '<table class="conflict-table"><thead><tr><th>' + esc(t('data.subject')) + '</th><th>' + esc(t('data.values_resolution')) + '</th><th>' + esc(t('data.state')) + '</th></tr></thead><tbody>' +
      rows.map(function (row) {
        return '<tr><td><span class="conflict-subject">' + esc(row.subject) + '</span>' +
          '<span class="conflict-scope">' + esc(row.scope) + (row.field ? ' · ' + esc(row.field) : '') + '</span></td>' +
          '<td><span class="conflict-value"><b>A</b> ' + esc(row.value_a) +
          '<span class="conflict-source"> · ' + esc(row.source_a_publisher) + '</span></span>' +
          '<span class="conflict-value"><b>B</b> ' + esc(row.value_b) +
          '<span class="conflict-source"> · ' + esc(row.source_b_publisher) + '</span></span>' +
          '<span class="conflict-resolution">' + esc(row.resolution) + '</span></td>' +
          '<td><span class="conflict-status ' + esc(row.status) + '">' + esc(row.status) + '</span></td></tr>';
      }).join('') + '</tbody></table></section>';
  }

  function dictionarySection() {
    const rows = stats.dictionary || [];
    if (!rows.length) return '<section class="data-section"><h3>' + esc(t('data.dictionary')) + '</h3><p>' + esc(t('data.dictionary_missing')) + '</p></section>';
    const tables = [];
    const byTable = {};
    rows.forEach(function (row) {
      if (!byTable[row.table]) {
        byTable[row.table] = { label: row.table_label, rows: [] };
        tables.push(row.table);
      }
      byTable[row.table].rows.push(row);
    });
    return '<section class="data-section"><h3>' + esc(t('data.dictionary')) + '</h3>' +
      '<p>' + esc(t('data.dictionary_note', {
        fields: fmtNum(rows.length), tables: fmtNum(tables.length)
      })) + '</p>' +
      '<div class="dictionary">' + tables.map(function (table) {
        const entry = byTable[table];
        const tableKey = 'dictionary.table.' + table.replace(/\.csv$/, '');
        return '<details><summary>' + esc(tOr(tableKey, entry.label)) + ' <span>' + esc(table) + ' · ' +
          esc(t('data.fields', { count: fmtNum(entry.rows.length) })) + '</span></summary>' +
          '<table><thead><tr><th>' + esc(t('data.field')) + '</th><th>' + esc(t('data.type')) +
          '</th><th>' + esc(t('data.description')) + '</th></tr></thead><tbody>' +
          entry.rows.map(function (row) {
            return '<tr><td class="field">' + esc(row.field) + '</td><td class="type">' +
              esc(row.type) + (row.required === 'yes' ? ' · ' + esc(t('data.required')) : '') + '</td><td>' +
              esc(row.description) + (row.allowed_values ? ' <small>' + esc(t('data.allowed', { values: row.allowed_values })) + '</small>' : '') +
              '</td></tr>';
          }).join('') + '</tbody></table></details>';
      }).join('') + '</div></section>';
  }

  function changelogSection() {
    const entries = stats.changelog || [];
    if (!entries.length) return '<section class="data-section"><h3>' + esc(t('data.changelog')) + '</h3><p>' + esc(t('data.no_changelog')) + '</p></section>';
    return '<section class="data-section"><h3>' + esc(t('data.changelog')) + '</h3><ul class="changelog">' +
      entries.map(function (entry) {
        return '<li><time>' + esc(fmtDate(entry.date)) + '</time><span><b>' +
          esc(entry.title) + '</b><br>' + entry.items.map(function (item) {
            return esc(item);
          }).join('<br>') + '</span></li>';
      }).join('') + '</ul></section>';
  }

  function renderData() {
    dom.exploreContent.hidden = true;
    dom.exploreContent.style.display = 'none';
    dom.viewPanel.hidden = false;

    const projectStats = stats.projects || {};
    const estateStats = stats.estates || {};
    const gapInfo = estateStats.gap_dispositions || {};
    const gapResolved = gapInfo.resolved || 0;
    const gapOpen = (gapInfo['unresolved-no-source'] || 0) + (gapInfo['unresolved-location-conflict'] || 0);
    const gapNotRequired = gapInfo['not-required-for-count'] || 0;
    const sectorCounts = projectStats.by_sector || {};
    const coverageByLayer = {};
    (stats.coverage || []).forEach(function (row) { coverageByLayer[row.layer] = row; });
    const transportCoverage = coverageByLayer.transport_psn || { current: 0, target: 35 };
    const roadCount = sectorCounts.road || 0;
    const generated = stats.generated_on ? fmtDate(stats.generated_on) : fmtDate(new Date().toISOString().slice(0, 10));

    const v = {
      total: fmtNum(projectStats.total || 0),
      investment: fmtNum(projectStats.with_investment || 0),
      progress: fmtNum(projectStats.with_progress || 0),
      length: fmtNum(projectStats.with_length || 0),
      unverified: fmtNum((projectStats.verification && projectStats.verification.unverified) || 0),
      current: fmtNum(transportCoverage.current),
      transportTarget: fmtNum(transportCoverage.target),
      factory: fmtNum(sectorCounts.factory || 0),
      energy: fmtNum(sectorCounts.energy || 0),
      water: fmtNum(sectorCounts.water || 0),
      industrial: fmtNum(estateStats.industrial || 0),
      sez: fmtNum(estateStats.sez || 0),
      estateTotal: fmtNum(estateStats.total || 0),
      both: fmtNum(estateStats.both || 0),
      unknown: fmtNum((estateStats.coordinate_sources || {}).unknown || 0),
      gapRows: fmtNum(estateStats.gap_rows || 0),
      resolved: fmtNum(gapResolved),
      gapOpen: fmtNum(gapOpen),
      notRequired: fmtNum(gapNotRequired),
      official: fmtNum((estateStats.coordinate_sources || {}).official || 0),
      osm: fmtNum((estateStats.coordinate_sources || {}).osm || 0),
      regency: fmtNum((estateStats.coordinate_sources || {}).regency || 0),
      manual: fmtNum((estateStats.coordinate_sources || {}).manual || 0),
      unknownPsn: fmtNum((projectStats.psn && projectStats.psn.unknown) || 0),
      roads: fmtNum(roadCount),
      approximate: fmtNum(projectStats.precision && projectStats.precision.approximate || 0),
      province: fmtNum(projectStats.precision && projectStats.precision.province || 0),
      single: fmtNum((projectStats.verification && projectStats.verification.single) || 0),
      dual: fmtNum((projectStats.verification && projectStats.verification.dual) || 0),
      claimed: fmtNum((stats.claims && stats.claims.projects_fully_claimed) || 0),
      claimsTotal: fmtNum((stats.claims && stats.claims.projects_total) || 0),
      claims: fmtNum((stats.claims && stats.claims.total) || 0),
      conflicts: fmtNum((stats.conflicts && stats.conflicts.total) || 0),
      conflictsOpen: fmtNum((stats.conflicts && stats.conflicts.open) || 0),
      records: fmtNum((stats.freshness && stats.freshness.records) || 0),
      nextDue: fmtDate(stats.freshness && stats.freshness.next_due),
      programmes: fmtNum((stats.programmes && stats.programmes.total) || 0),
      lead: fmtNum((stats.programmes && stats.programmes.with_lead) || 0),
      links: fmtNum((stats.programmes && stats.programmes.with_projects) || 0),
      targets: fmtNum((stats.programmes && stats.programmes.with_target) || 0),
      indicators: fmtNum((stats.indicators && stats.indicators.total) || 0),
      indicatorValues: fmtNum((stats.indicators && stats.indicators.values) || 0),
      phases: fmtNum((stats.phases && stats.phases.total) || 0),
      indicatorProjects: fmtNum((stats.indicators && stats.indicators.projects_with_indicators) || 0),
      companiesTotal: fmtNum((stats.organizations && stats.organizations.total) || 0),
      companiesLinked: fmtNum((stats.organizations && stats.organizations.with_links) || 0),
      companyLinks: fmtNum((stats.organizations && stats.organizations.links) || 0),
      companyGap: fmtNum(Math.max(300 - ((stats.organizations && stats.organizations.total) || 0), 0))
    };

    dom.viewPanel.innerHTML =
      '<div class="data-view">' +
      '<h2>' + esc(t('data.title')) + '</h2>' +
      '<p class="lede">' + esc(t('data.lede')) + '</p>' +

      '<section class="data-section"><h3>' + esc(t('data.coverage')) + '</h3>' + coverageRows() +
      '<p style="margin-top:7px;color:var(--muted);font-size:9px">' +
      esc(t('data.generated', { date: generated, as_of: fmtDate(stats.data_as_of) })) + '</p></section>' +

      chartsSection() +

      '<section class="data-section"><h3>' + esc(t('data.programme_register')) + '</h3>' +
      '<p>' + esc(t('data.programme_lede', {
        total: v.programmes, lead: v.lead, links: v.links, target: v.targets
      })) + '</p>' +
      '<p><a href="#/programmes">' + esc(t('data.open_programmes')) + '</a></p></section>' +

      '<section class="data-section"><h3>' + esc(t('data.indicators')) + '</h3>' +
      '<p>' + esc(t('data.indicator_lede', {
        indicators: v.indicators, values: v.indicatorValues,
        phases: v.phases, projects: v.indicatorProjects
      })) + '</p></section>' +

      claimsSection() + freshnessSection() +

      '<section class="data-section"><h3>' + esc(t('data.what')) + '</h3>' +
      '<p>' + esc(t('data.what_body')) + '</p>' +
      '<p><b>' + esc(t('data.verification_rule').split('.')[0]) + '.</b> ' +
      esc(t('data.verification_rule').split('.').slice(1).join('.').trim()) + '</p></section>' +

      '<section class="data-section"><h3>' + esc(t('data.status_definitions')) + '</h3><ul class="def-list">' +
      STATUS_ORDER.map(function (status) {
        return '<li><b>' + esc(statusLabel(status)) + '</b><span>' +
          esc(t('status.' + status + '.meaning')) + '</span></li>';
      }).join('') + '</ul></section>' +

      '<section class="data-section"><h3>' + esc(t('data.inclusion')) + '</h3>' +
      '<p>' + esc(t('data.inclusion_body')) + '</p>' +
      '<p>' + esc(t('data.inclusion_body2')) + '</p></section>' +

      '<section class="data-section"><h3>' + esc(t('data.known_gaps')) + '</h3><ul class="gap-list">' +
      '<li>' + esc(t('data.gap_projects', v)) + '</li>' +
      '<li>' + esc(t('data.gap_transport', v)) + '</li>' +
      '<li>' + esc(t('data.gap_industry', v)) + '</li>' +
      '<li>' + esc(t('data.gap_programmes', v)) + '</li>' +
      '<li>' + esc(t('data.gap_companies', v)) + '</li>' +
      '<li>' + esc(t('data.gap_estates', v)) + '</li>' +
      '<li>' + esc(t('data.gap_estate_coords', v)) + '</li>' +
      '<li>' + esc(t('data.gap_corridors')) + '</li>' +
      '<li>' + esc(t('data.gap_psn', v)) + '</li>' +
      '<li>' + esc(t('data.gap_verification', v)) + '</li>' +
      '<li>' + esc(t('data.gap_claims', v)) + '</li>' +
      '<li>' + esc(t('data.gap_conflicts', v)) + '</li>' +
      '<li>' + esc(t('data.gap_freshness', v)) + '</li>' +
      '</ul></section>' +

      conflictsSection() +

      '<section class="data-section"><h3>' + esc(t('data.source_register')) + '</h3>' + sourceRegister() + '</section>' +

      '<section class="data-section"><h3>' + esc(t('data.downloads')) + '</h3>' + downloadList() + '</section>' +

      dictionarySection() +
      changelogSection() +
      '</div>';
  }

  /* ---------- render orchestration ---------- */

  function renderAll() {
    const active = state.view === 'project' ? 'explore' : state.view;
    const appMain = document.querySelector('.app-main');
    if (appMain) {
      const wide = active === 'data' || active === 'programmes' ||
        active === 'estates' || active === 'companies' || active === 'corridors';
      appMain.classList.toggle('is-wide', wide);
    }
    renderHeader();
    renderTabs();

    if (state.view === 'explore' || state.view === 'project') {
      renderExplore();
    } else if (state.view === 'corridors') {
      renderCorridors();
    } else if (state.view === 'estates') {
      renderEstates();
    } else if (state.view === 'programmes') {
      renderProgrammes();
    } else if (state.view === 'companies') {
      renderCompanies();
    } else if (state.view === 'data') {
      renderData();
    }

    renderDrawer();
    renderMap();
    requestAnimationFrame(function () {
      if (window.AtlasMap) window.AtlasMap.resize();
    });
  }

  /* ---------- mobile sheet ---------- */

  function sheetSnaps() {
    const viewport = window.innerHeight - (mobileQuery.matches ? 56 : 64);
    return [220, Math.round(viewport * 0.52), viewport - 12];
  }

  function sheetSnapForView() {
    const snaps = sheetSnaps();
    if (state.view === 'data' || state.view === 'programmes') return snaps[2];
    if (state.view === 'corridors' || state.view === 'estates') return snaps[1];
    return snaps[0];
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
    setSheetHeight(sheetSnapForView());
  }

  function bindSheet() {
    if (!dom.sheetHandle) return;

    dom.sheetHandle.addEventListener('pointerdown', function (event) {
      if (!mobileQuery.matches) return;
      const startHeight = dom.rail.getBoundingClientRect().height;
      sheetDrag = { startY: event.clientY, startHeight: startHeight, moved: false };
      dom.rail.classList.add('is-dragging');
      dom.sheetHandle.setPointerCapture(event.pointerId);
      event.preventDefault();
    });

    dom.sheetHandle.addEventListener('pointermove', function (event) {
      if (!sheetDrag) return;
      if (Math.abs(event.clientY - sheetDrag.startY) > 6) sheetDrag.moved = true;
      const height = sheetDrag.startHeight + (sheetDrag.startY - event.clientY);
      setSheetHeight(height, false);
    });

    dom.sheetHandle.addEventListener('pointerup', function (event) {
      if (!sheetDrag) return;
      const drag = sheetDrag;
      sheetDrag = null;
      dom.rail.classList.remove('is-dragging');
      const snaps = sheetSnaps();
      if (!drag.moved) {
        // A tap cycles peek -> half -> full -> peek, so filters are reachable
        // without discovering the drag gesture.
        setSheetHeight(snaps[(sheetSnapIndex + 1) % snaps.length]);
      } else {
        const current = dom.rail.getBoundingClientRect().height;
        const nearest = snaps.reduce(function (best, snap) {
          return Math.abs(snap - current) < Math.abs(best - current) ? snap : best;
        }, snaps[0]);
        setSheetHeight(nearest);
      }
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
      toast(ok ? t('toast.link_copied') : t('toast.copy_manual'));
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(url).then(function () { toast(t('toast.link_copied')); }).catch(fallback);
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
          setSheetHeight((view === 'data' || view === 'programmes') ? snaps[2] : snaps[1]);
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

    dom.searchGroups.addEventListener('click', function (event) {
      const button = event.target.closest('[data-search-view]');
      if (!button) return;
      const view = button.getAttribute('data-search-view');
      state.view = view;
      state.projectId = null;
      state.corridorId = null;
      commit(true);
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
      const sortButton = event.target.closest('[data-coverage-sort]');
      if (sortButton) {
        const key = sortButton.getAttribute('data-coverage-sort');
        if (state.coverageSort.key === key) {
          state.coverageSort.dir *= -1;
        } else {
          state.coverageSort = { key: key, dir: key === 'layer' ? 1 : -1 };
        }
        const scrollTop = dom.viewPanel.scrollTop;
        renderData();
        dom.viewPanel.scrollTop = scrollTop;
        const next = dom.viewPanel.querySelector('[data-coverage-sort="' + key + '"]');
        if (next) next.focus();
        return;
      }
      const exporter = event.target.closest('[data-export]');
      if (exporter) {
        handleExport(exporter.getAttribute('data-export'));
        return;
      }
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
      '<div class="legend-sector">' + esc(t('map.legend_note')) + '</div>';
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
    dom.searchGroups = $('search-groups');
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
    dom.mapCaptionText = $('map-caption-text');
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
    dom.tabCountProgrammes = $('tab-count-programmes');
    dom.tabCountCompanies = $('tab-count-companies');
    dom.layerProjects = $('layer-projects');
    dom.layerLabels = $('layer-labels');
    dom.legendBody = $('legend-body');
    dom.mapWrap = document.querySelector('.map-wrap');

    if (!features.length) {
      dom.resultCount.textContent = t('result.data_not_loaded');
      dom.projectList.innerHTML = '<li><div class="list-empty"><h3>' + esc(t('result.no_data_title')) + '</h3>' +
        '<p>' + esc(t('result.no_data_body')) + '</p></div></li>';
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
    if (state.view === 'programmes') ensureProgrammes();
    if (state.view === 'companies') ensureCompanies();

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
