/* Shared vocabulary for the atlas UI and map. */
window.ATLAS = {
  STATUS: {
    under_construction: { label: 'Under construction', short: 'Build', color: '#c2410c' },
    planned: { label: 'Planned', short: 'Planned', color: '#1d4ed8' },
    operating: { label: 'Operating', short: 'Open', color: '#0f766e' },
    recently_completed: { label: 'Recently completed', short: 'Done', color: '#15803d' },
    stalled: { label: 'Stalled', short: 'Stalled', color: '#b42318' }
  },
  STATUS_ORDER: ['under_construction', 'planned', 'operating', 'recently_completed', 'stalled'],
  SECTORS: {
    road: { label: 'Road', plural: 'Roads', short: 'Road', icon: '#i-road' },
    railway: { label: 'Railway', plural: 'Railways', short: 'Rail', icon: '#i-railway' },
    airport: { label: 'Airport', plural: 'Airports', short: 'Air', icon: '#i-airport' },
    seaport: { label: 'Seaport', plural: 'Seaports', short: 'Sea', icon: '#i-seaport' },
    factory: { label: 'Factory', plural: 'Factories', short: 'Factory', icon: '#i-factory' }
  },
  SECTOR_ORDER: ['road', 'railway', 'airport', 'seaport', 'factory'],
  STALE_DAYS: 183,
  VERIFY_MONTHS: 6
};
