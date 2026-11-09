/* Shared vocabulary for the atlas UI and map. */
window.ATLAS = {
  STATUS: {
    under_construction: { label: 'Under construction', short: 'Build', color: '#c2410c' },
    planned: { label: 'Planned', short: 'Planned', color: '#1d4ed8' },
    operating: { label: 'Operating', short: 'Open', color: '#0f766e' },
    recently_completed: { label: 'Recently completed', short: 'Done', color: '#15803d' },
    stalled: { label: 'Stalled', short: 'Stalled', color: '#b42318' },
    unknown: { label: 'Status not sourced', short: 'Unknown', color: '#667085' }
  },
  STATUS_ORDER: ['under_construction', 'planned', 'operating', 'recently_completed', 'stalled', 'unknown'],
  SECTORS: {
    road: { label: 'Road', plural: 'Roads', short: 'Road', icon: '#i-road' },
    railway: { label: 'Railway', plural: 'Railways', short: 'Rail', icon: '#i-railway' },
    airport: { label: 'Airport', plural: 'Airports', short: 'Air', icon: '#i-airport' },
    seaport: { label: 'Seaport', plural: 'Seaports', short: 'Sea', icon: '#i-seaport' },
    factory: { label: 'Factory', plural: 'Factories', short: 'Factory', icon: '#i-factory' },
    energy: { label: 'Energy', plural: 'Energy', short: 'Energy', icon: '#i-energy' },
    water: { label: 'Water', plural: 'Water', short: 'Water', icon: '#i-water' },
    urban: { label: 'Urban', plural: 'Urban', short: 'Urban', icon: '#i-urban' },
    coastal: { label: 'Coastal', plural: 'Coastal', short: 'Coast', icon: '#i-coastal' },
    housing: { label: 'Housing', plural: 'Housing', short: 'Housing', icon: '#i-housing' },
    technology: { label: 'Technology', plural: 'Technology', short: 'Tech', icon: '#i-technology' },
    education: { label: 'Education', plural: 'Education', short: 'Education', icon: '#i-education' },
    tourism: { label: 'Tourism', plural: 'Tourism', short: 'Tourism', icon: '#i-tourism' },
    agriculture: { label: 'Agriculture', plural: 'Agriculture', short: 'Agriculture', icon: '#i-agriculture' }
  },
  SECTOR_ORDER: [
    'road', 'railway', 'airport', 'seaport', 'factory', 'energy', 'water',
    'urban', 'coastal', 'housing', 'technology', 'education', 'tourism',
    'agriculture'
  ],
  PROGRAMME_THEMES: {
    energy: { label: 'Energy', color: '#b45309' },
    economy: { label: 'Economy', color: '#0f766e' },
    border: { label: 'Border areas', color: '#1d4ed8' },
    transport: { label: 'Transport', color: '#c2410c' },
    tourism: { label: 'Tourism', color: '#7c3aed' },
    industry: { label: 'Industry', color: '#475569' },
    food: { label: 'Food', color: '#15803d' },
    urban: { label: 'Urban', color: '#334155' },
    water: { label: 'Water', color: '#0369a1' },
    health: { label: 'Health', color: '#be123c' },
    education: { label: 'Education', color: '#4338ca' },
    social: { label: 'Social', color: '#a16207' },
    environment: { label: 'Environment', color: '#047857' }
  },
  PROGRAMME_THEME_ORDER: [
    'energy', 'economy', 'border', 'transport', 'tourism', 'industry', 'food',
    'urban', 'water', 'health', 'education', 'social', 'environment'
  ],
  STALE_DAYS: 183,
  VERIFY_MONTHS: 6
};
