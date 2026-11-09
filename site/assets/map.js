/* Leaflet map: bundled basemap, sector markers and clustering. */
(function () {
  'use strict';

  const A = window.ATLAS || {};
  const STATUS = A.STATUS || {};
  const STATUS_ORDER = A.STATUS_ORDER || [];
  const I18N = window.AtlasI18n || {};

  function tt(key, vars) {
    return I18N.t ? I18N.t(key, vars) : key;
  }

  function projectName(project) {
    return I18N.entityName ? I18N.entityName('project', project) : project.name;
  }

  function statusLabel(status) {
    return I18N.t ? I18N.t('status.' + status + '.label') : status;
  }
  const SECTOR_ICON = {};
  Object.keys(A.SECTORS || {}).forEach(function (key) {
    SECTOR_ICON[key] = A.SECTORS[key].icon;
  });

  let map = null;
  let cluster = null;
  let markers = new Map();
  let selectedId = null;
  let selectedLabel = null;
  let current = [];
  let cityMajor = null;
  let cityMinor = null;
  let labelsOn = true;
  let projectsOn = true;
  let handlers = { select: function () {} };
  let reduceMotion = false;

  function escapeHtml(value) {
    return String(value == null ? '' : value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function statusColor(status) {
    return (STATUS[status] && STATUS[status].color) || '#667085';
  }

  function pinIcon(project, selected) {
    const size = selected ? 38 : 28;
    const symbol = SECTOR_ICON[project.sector] || '#i-place';
    const cls = selected ? 'pin is-selected' : 'pin';
    return L.divIcon({
      className: 'pin-icon',
      html:
        '<div class="' + cls + '" style="--c:' + statusColor(project.status) + '">' +
        '<svg aria-hidden="true"><use href="' + symbol + '"></use></svg></div>',
      iconSize: [size, size],
      iconAnchor: [size / 2, size / 2]
    });
  }

  function clusterIcon(clusterGroup) {
    const children = clusterGroup.getAllChildMarkers();
    const counts = {};
    children.forEach(function (marker) {
      const status = marker.options.projectStatus || 'under_construction';
      counts[status] = (counts[status] || 0) + 1;
    });
    let cursor = 0;
    const stops = [];
    STATUS_ORDER.forEach(function (status) {
      const count = counts[status] || 0;
      if (!count) return;
      const start = (cursor / children.length) * 360;
      cursor += count;
      const end = (cursor / children.length) * 360;
      stops.push(statusColor(status) + ' ' + start + 'deg ' + end + 'deg');
    });
    const ring = 'conic-gradient(' + stops.join(',') + ')';
    return L.divIcon({
      className: 'cluster-icon',
      html:
        '<div class="cluster" role="img" aria-label="' + escapeHtml(tt('map.cluster', { count: children.length })) +
        '" style="--ring:' + ring + '"><span>' +
        children.length + '</span></div>',
      iconSize: [42, 42],
      iconAnchor: [21, 21]
    });
  }

  function addCityLabels(basemap) {
    cityMajor = L.layerGroup();
    cityMinor = L.layerGroup();
    const majorNames = {
      Jakarta: true, Surabaya: true, Medan: true, Makassar: true,
      Bandung: true, Semarang: true, Palembang: true, Denpasar: true
    };
    (basemap.places || []).forEach(function (place) {
      const major = !!majorNames[place.name] || place.capital;
      const label = L.marker([place.lat, place.lon], {
        icon: L.divIcon({
          className: 'city-label-icon',
          html:
            '<span class="city-label' + (major ? ' major' : '') + '">' +
            '<i></i>' + escapeHtml(place.name) + '</span>',
          iconSize: [0, 0],
          iconAnchor: [0, 0]
        }),
        interactive: false,
        keyboard: false
      });
      label.addTo(major ? cityMajor : cityMinor);
    });
  }

  function syncCityLabels() {
    if (!map || !cityMajor || !cityMinor) return;
    const zoom = map.getZoom();
    if (labelsOn && zoom >= 5) {
      if (!map.hasLayer(cityMajor)) cityMajor.addTo(map);
    } else if (map.hasLayer(cityMajor)) {
      map.removeLayer(cityMajor);
    }
    if (labelsOn && zoom >= 7) {
      if (!map.hasLayer(cityMinor)) cityMinor.addTo(map);
    } else if (map.hasLayer(cityMinor)) {
      map.removeLayer(cityMinor);
    }
  }

  function init(options) {
    if (map) return map;
    handlers = Object.assign(handlers, options || {});
    reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    map = L.map('map', {
      zoomControl: false,
      minZoom: 3,
      maxZoom: 12,
      worldCopyJump: false,
      attributionControl: true,
      zoomSnap: 0.5
    }).setView([-2.4, 118.0], 5);

    L.control.zoom({ position: 'bottomright' }).addTo(map);
    L.control.scale({ position: 'bottomright', imperial: false, maxWidth: 120 }).addTo(map);

    const basemap = window.BASEMAP || {
      countries: { features: [] },
      provinces: { features: [] },
      lakes: { features: [] },
      rivers: { features: [] },
      urban: { features: [] },
      places: []
    };

    L.geoJSON(basemap.countries, {
      interactive: false,
      style: function (feature) {
        return feature.properties.name === 'Indonesia'
          ? { color: '#c9cdd4', weight: 1.0, fillColor: '#f4f1e8', fillOpacity: 1 }
          : { color: '#d9d5cc', weight: 0.7, fillColor: '#edeae2', fillOpacity: 1 };
      }
    }).addTo(map);

    L.geoJSON(basemap.urban, {
      interactive: false,
      style: { stroke: false, fillColor: '#e7e1d4', fillOpacity: 0.55 }
    }).addTo(map);

    L.geoJSON(basemap.provinces, {
      interactive: false,
      style: { color: '#d5d0c4', weight: 0.7, opacity: 0.9, fill: false }
    }).addTo(map);

    L.geoJSON(basemap.lakes, {
      interactive: false,
      style: { color: '#c9d8e2', weight: 0.7, fillColor: '#dce9f2', fillOpacity: 1 }
    }).addTo(map);

    L.geoJSON(basemap.rivers, {
      interactive: false,
      style: { color: '#c9d8e2', weight: 0.6, opacity: 0.85 }
    }).addTo(map);

    map.attributionControl.addAttribution(
      escapeHtml(tt('map.basemap')) +
      ' <a href="https://www.naturalearthdata.com/">Natural Earth</a>'
    );

    addCityLabels(basemap);
    map.on('zoomend', syncCityLabels);
    syncCityLabels();

    cluster = L.markerClusterGroup({
      showCoverageOnHover: false,
      maxClusterRadius: 60,
      disableClusteringAtZoom: 7,
      spiderfyOnMaxZoom: true,
      zoomToBoundsOnClick: true,
      removeOutsideVisibleBounds: true,
      iconCreateFunction: clusterIcon
    });
    map.addLayer(cluster);

    map.on('click', function () {
      if (handlers.deselect) handlers.deselect();
    });

    return map;
  }

  function markerFor(project) {
    const marker = L.marker([project.lat, project.lon], {
      icon: pinIcon(project, project.id === selectedId),
      title: projectName(project) + ' — ' + statusLabel(project.status),
      alt: projectName(project) + ' — ' + statusLabel(project.status),
      riseOnHover: true,
      keyboard: true,
      projectStatus: project.status
    });
    marker._project = project;
    marker.on('click', function (event) {
      L.DomEvent.stopPropagation(event);
      handlers.select(project.id, { source: 'map' });
    });
    markers.set(project.id, marker);
    return marker;
  }

  function setProjects(projects) {
    if (!map) return;
    const next = new Map(projects.map(function (project) { return [project.id, project]; }));

    const removed = [];
    markers.forEach(function (marker, id) {
      if (!next.has(id)) removed.push(id);
    });
    removed.forEach(function (id) {
      const marker = markers.get(id);
      cluster.removeLayer(marker);
      markers.delete(id);
      if (selectedId === id) clearSelection();
    });

    projects.forEach(function (project) {
      const existing = markers.get(project.id);
      if (existing) {
        existing.options.projectStatus = project.status;
        existing._project = project;
        if (project.id === selectedId) existing.setIcon(pinIcon(project, true));
      } else {
        cluster.addLayer(markerFor(project));
      }
    });

    current = projects.slice();
  }

  function clearSelection() {
    if (selectedId && markers.has(selectedId)) {
      const marker = markers.get(selectedId);
      if (marker._project) marker.setIcon(pinIcon(marker._project, false));
    }
    if (selectedLabel) {
      map.removeLayer(selectedLabel);
      selectedLabel = null;
    }
    selectedId = null;
  }

  function select(id, options) {
    options = options || {};
    if (!map || !markers.has(id)) return;
    const marker = markers.get(id);
    const project = marker._project || current.find(function (item) { return item.id === id; });
    if (!project) return;

    if (selectedId && selectedId !== id && markers.has(selectedId)) {
      markers.get(selectedId).setIcon(pinIcon(markers.get(selectedId)._project, false));
    }
    selectedId = id;
    marker._project = project;
    marker.setIcon(pinIcon(project, true));

    if (selectedLabel) {
      map.removeLayer(selectedLabel);
      selectedLabel = null;
    }

    const targetZoom = Math.max(map.getZoom(), 8);
    const drawerWidth = options.drawerWidth || 0;
    const latlng = L.latLng(project.lat, project.lon);
    const point = map.project(latlng, targetZoom);
    const center = map.unproject(point.add([drawerWidth / 2, 0]), targetZoom);
    map.setView(center, targetZoom, { animate: !reduceMotion });

    selectedLabel = L.tooltip({
      permanent: true,
      direction: 'right',
      offset: [20, 0],
      className: 'pin-label',
      opacity: 1
    })
      .setLatLng(latlng)
      .setContent(escapeHtml(projectName(project)))
      .addTo(map);
  }

  function fitAll(bottomPadding) {
    if (!map) return;
    // Always open on the whole archipelago, not on the current project extent.
    const indonesia = L.latLngBounds([[-11.5, 94.5], [6.5, 141.5]]);
    map.fitBounds(indonesia, {
      paddingTopLeft: [0, 0],
      paddingBottomRight: [0, bottomPadding || 0],
      animate: false
    });
  }

  function setLabels(on) {
    labelsOn = !!on;
    syncCityLabels();
  }

  function setProjectsVisible(on) {
    projectsOn = !!on;
    if (!map || !cluster) return;
    if (projectsOn) {
      if (!map.hasLayer(cluster)) map.addLayer(cluster);
    } else if (map.hasLayer(cluster)) {
      map.removeLayer(cluster);
    }
  }

  function resize() {
    if (map) setTimeout(function () { map.invalidateSize(); }, 40);
  }

  window.AtlasMap = {
    init: init,
    setProjects: setProjects,
    select: select,
    clearSelection: clearSelection,
    fitAll: fitAll,
    setLabels: setLabels,
    setProjectsVisible: setProjectsVisible,
    resize: resize,
    getMap: function () { return map; }
  };
})();
