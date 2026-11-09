/* Locale runtime: catalogue lookup, entity text and Intl formatting. */
(function () {
  'use strict';

  const payload = window.INFRA_I18N || {};
  const locale = payload.locale === 'id' ? 'id' : 'en';
  const messages = payload.messages || {};
  const entities = payload.entities || {};
  const missingLabel = payload.missing_label || 'Not yet translated';
  const intlLocale = locale === 'id' ? 'id-ID' : 'en-GB';

  function t(key, vars) {
    let text = messages[key];
    if (text === undefined) text = key;
    if (vars) {
      Object.keys(vars).forEach(function (name) {
        text = String(text).split('{' + name + '}').join(String(vars[name]));
      });
    }
    return text;
  }

  const PROVINCES = {
    "Aceh": ["Aceh", "Aceh"],
    "North Sumatra": ["North Sumatra", "Sumatera Utara"],
    "West Sumatra": ["West Sumatra", "Sumatera Barat"],
    "Riau": ["Riau", "Riau"],
    "Riau Islands": ["Riau Islands", "Kepulauan Riau"],
    "Jambi": ["Jambi", "Jambi"],
    "Bengkulu": ["Bengkulu", "Bengkulu"],
    "South Sumatra": ["South Sumatra", "Sumatera Selatan"],
    "Lampung": ["Lampung", "Lampung"],
    "Bangka Belitung": ["Bangka Belitung", "Kepulauan Bangka Belitung"],
    "Banten": ["Banten", "Banten"],
    "DKI Jakarta": ["DKI Jakarta", "DKI Jakarta"],
    "West Java": ["West Java", "Jawa Barat"],
    "Central Java": ["Central Java", "Jawa Tengah"],
    "DI Yogyakarta": ["DI Yogyakarta", "DI Yogyakarta"],
    "East Java": ["East Java", "Jawa Timur"],
    "Bali": ["Bali", "Bali"],
    "West Nusa Tenggara": ["West Nusa Tenggara", "Nusa Tenggara Barat"],
    "East Nusa Tenggara": ["East Nusa Tenggara", "Nusa Tenggara Timur"],
    "West Kalimantan": ["West Kalimantan", "Kalimantan Barat"],
    "Central Kalimantan": ["Central Kalimantan", "Kalimantan Tengah"],
    "South Kalimantan": ["South Kalimantan", "Kalimantan Selatan"],
    "East Kalimantan": ["East Kalimantan", "Kalimantan Timur"],
    "North Kalimantan": ["North Kalimantan", "Kalimantan Utara"],
    "North Sulawesi": ["North Sulawesi", "Sulawesi Utara"],
    "Gorontalo": ["Gorontalo", "Gorontalo"],
    "Central Sulawesi": ["Central Sulawesi", "Sulawesi Tengah"],
    "West Sulawesi": ["West Sulawesi", "Sulawesi Barat"],
    "South Sulawesi": ["South Sulawesi", "Sulawesi Selatan"],
    "Southeast Sulawesi": ["Southeast Sulawesi", "Sulawesi Tenggara"],
    "Maluku": ["Maluku", "Maluku"],
    "North Maluku": ["North Maluku", "Maluku Utara"],
    "Papua": ["Papua", "Papua"],
    "West Papua": ["West Papua", "Papua Barat"],
    "Southwest Papua": ["Southwest Papua", "Papua Barat Daya"],
    "Central Papua": ["Central Papua", "Papua Tengah"],
    "South Papua": ["South Papua", "Papua Selatan"],
    "Highland Papua": ["Highland Papua", "Papua Pegunungan"],
    "Indonesia": ["Indonesia", "Indonesia"],
    "Eastern Indonesia": ["Eastern Indonesia", "Indonesia Timur"]
  };

  const UNITS_ID = {
    "million m3": "juta m³",
    "ktpa copper cathode": "ktpa katoda tembaga",
    "ktpa stainless steel": "ktpa baja nirkarat",
    "ktpa ethylene": "ktpa etilena",
    "ktpa concentrate": "ktpa konsentrat",
    "ktpa crude steel": "ktpa baja mentah",
    "ktpa Ni in MHP": "ktpa Ni dalam MHP",
    "ktpa Ni in ferronickel": "ktpa Ni dalam feronikel",
    "ktpa Ni+Co in MHP": "ktpa Ni+Co dalam MHP",
    "ktpa Ni in NPI": "ktpa Ni dalam NPI",
    "ktpa steel slab": "ktpa slab baja",
    "ktpa steel": "ktpa baja",
    "ktpa anode material": "ktpa bahan anoda",
    "GWh/y cells": "GWh/tahun sel",
    "m runway": "m landasan pacu",
    "kbd crude": "kbd minyak mentah",
    "MWp launched": "MWp terpasang"
  };

  function unitLabel(value) {
    if (!value) return '';
    return locale === 'id' ? (UNITS_ID[value] || value) : value;
  }

  const ISLANDS = {
    "Sumatra": ["Sumatra", "Sumatra"],
    "Java": ["Java", "Jawa"],
    "Kalimantan": ["Kalimantan", "Kalimantan"],
    "Sulawesi": ["Sulawesi", "Sulawesi"],
    "Papua": ["Papua", "Papua"],
    "Bali-Nusa Tenggara": ["Bali-Nusa Tenggara", "Bali–Nusa Tenggara"],
    "Maluku": ["Maluku", "Maluku"],
    "National": ["National", "Nasional"]
  };

  function provinceName(value) {
    return String(value || '').split(';').map(function (part) {
      const name = part.trim();
      const record = PROVINCES[name];
      return record ? record[locale === 'id' ? 1 : 0] : name;
    }).filter(Boolean).join(', ');
  }

  function islandName(value) {
    const record = ISLANDS[value];
    return record ? record[locale === 'id' ? 1 : 0] : String(value || '');
  }

  function entity(type, id, field, fallback) {
    const record = entities[type + ':' + id];
    if (record && record[field] !== undefined && record[field] !== '') return record[field];
    return fallback == null ? '' : fallback;
  }

  function entityName(type, record) {
    return entity(type, record.id, 'name', record.name || '');
  }

  function entitySummary(type, record, localeField, fallbackField) {
    const value = entity(type, record.id, 'summary', '');
    if (value) return value;
    if (localeField && record[localeField]) return record[localeField];
    if (fallbackField && record[fallbackField]) return record[fallbackField];
    return '';
  }

  function fmtNum(value) {
    const number = Number(value);
    if (!isFinite(number)) return String(value == null ? '' : value);
    return new Intl.NumberFormat(intlLocale, { maximumFractionDigits: 1 }).format(number);
  }

  function fmtCoord(value) {
    const number = Number(value);
    if (!isFinite(number)) return String(value == null ? '' : value);
    return new Intl.NumberFormat(intlLocale, {
      minimumFractionDigits: 4, maximumFractionDigits: 5
    }).format(number);
  }

  function fmtDate(value) {
    if (!value) return '';
    const parsed = new Date(String(value) + 'T00:00:00');
    if (isNaN(parsed.getTime())) return String(value);
    return new Intl.DateTimeFormat(intlLocale, {
      day: 'numeric', month: 'short', year: 'numeric'
    }).format(parsed);
  }

  function fmtDateLong(value) {
    if (!value) return '';
    const parsed = new Date(String(value) + 'T00:00:00');
    if (isNaN(parsed.getTime())) return String(value);
    return new Intl.DateTimeFormat(intlLocale, {
      day: 'numeric', month: 'long', year: 'numeric'
    }).format(parsed);
  }

  function fmtList(items) {
    if (!items || !items.length) return '';
    try {
      return new Intl.ListFormat(intlLocale, { style: 'long', type: 'conjunction' }).format(items);
    } catch (error) {
      return items.join(', ');
    }
  }

  function apply(root) {
    const scope = root || document;
    scope.querySelectorAll('[data-i18n]').forEach(function (element) {
      const key = element.getAttribute('data-i18n');
      if (key) element.textContent = t(key);
    });
    scope.querySelectorAll('[data-i18n-placeholder]').forEach(function (element) {
      element.setAttribute('placeholder', t(element.getAttribute('data-i18n-placeholder')));
    });
    scope.querySelectorAll('[data-i18n-aria-label]').forEach(function (element) {
      element.setAttribute('aria-label', t(element.getAttribute('data-i18n-aria-label')));
    });
    scope.querySelectorAll('[data-i18n-title]').forEach(function (element) {
      element.setAttribute('title', t(element.getAttribute('data-i18n-title')));
    });
  }

  function bindLanguageSwitch() {
    const links = document.querySelectorAll('[data-lang-target]');
    links.forEach(function (link) {
      const target = link.getAttribute('data-lang-target');
      if (target === locale) link.setAttribute('aria-current', 'page');
      link.addEventListener('click', function (event) {
        event.preventDefault();
        const base = link.getAttribute('href') || ('../' + target + '/index.html');
        location.href = base + (location.hash || '#/explore');
      });
    });
  }

  function boot() {
    document.documentElement.lang = locale;
    document.documentElement.setAttribute('data-locale', locale);
    apply(document);
    bindLanguageSwitch();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }

  window.AtlasI18n = {
    locale: locale,
    t: t,
    entity: entity,
    entityName: entityName,
    entitySummary: entitySummary,
    provinceName: provinceName,
    islandName: islandName,
    unitLabel: unitLabel,
    fmtNum: fmtNum,
    fmtCoord: fmtCoord,
    fmtDate: fmtDate,
    fmtDateLong: fmtDateLong,
    fmtList: fmtList,
    apply: apply,
    missingLabel: missingLabel
  };
})();
