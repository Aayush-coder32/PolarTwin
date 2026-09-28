// Local illustrations keep image cards available in deployments that block
// hotlinked images. These are concept art, not photographs of real stations.
const image = (file, alt) => ({ url: `/assets/${file}.svg`, alt, source: 'PolarTwin illustrative artwork' });
const base = image('antarctic-base', 'Illustration of a research station on Antarctic ice');
const weather = image('weather-station', 'Illustration of an automatic weather station on Antarctic ice');
const solar = image('solar-station', 'Illustration of solar panels at a polar research station');
const traverse = image('polar-traverse', 'Illustration of an Antarctic supply traverse');
const lab = image('polar-lab', 'Illustration of a polar research laboratory');

export const categoryImages = {
  overview: [base, weather],
  'digital-twin': [base, traverse],
  environment: [weather, base],
  energy: [solar, weather],
  infrastructure: [base, lab],
  equipment: [weather, solar],
  maintenance: [traverse, weather],
  logistics: [traverse, base],
  inventory: [traverse, lab],
  alerts: [weather, traverse],
  emergency: [traverse, weather],
  analytics: [base, weather],
  reports: [lab, base],
  polarai: [lab, weather],
  settings: [lab, base],
};
