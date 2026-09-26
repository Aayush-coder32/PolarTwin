// Remote editorial photographs grouped by the matching PolarTwin module.
// Sources are external publishers; these are illustrative Antarctic/polar images,
// not photographs of Maitri or Bharati unless explicitly identified in the caption.
const pair = (items) => items.map(([url, alt, source]) => ({ url, alt, source }));
export const categoryImages = {
  overview: pair([
    ['https://bcp.cdnchinhphu.vn/Uploaded/nguyendieuhuong/2020_12_23/1-1608689061084.jpg', 'Antarctic research base beside an ice-covered coast', 'Vietnam Government News'],
    ['https://www.antarctica.gov.au/site/assets/files/48844/rs24868_mg_0018.600x400.jpg', 'Research station standing on an Antarctic snow plain', 'Australian Antarctic Program'],
  ]),
  'digital-twin': pair([
    ['https://cdn.forumcomm.com/dims4/default/df7af95/2147483647/strip/true/crop/5184x3456%2B0%2B0/resize/840x560%21/quality/90/?url=https%3A%2F%2Ffcc-cue-exports-brightspot.s3.us-west-2.amazonaws.com%2Ffccnn%2Fbinary%2F1dym8xru0w1wc88e4w8iykyzzw7juga99_binary_807413.jpg', 'Elevated research building at the South Pole', 'InForum'],
    ['https://antarctic-logistics.com/wp-content/uploads/2016/08/5425658002_c56295dcd5_b-1024x681.jpg', 'Modular research station buildings in Antarctica', 'Antarctic Logistics & Expeditions'],
  ]),
  environment: pair([
    ['https://media.tag24.de/1200x800/g/w/gwc4v5xhi4l1fghipbzbvn3hk578go68.jpg', 'Antarctic glacier front, snow-covered mountains and sea ice', 'Tag24'],
    ['https://mediasvc.eurekalert.org/Api/v1/Multimedia/fe282343-d875-40c5-a904-c3ef6e36ace9/Rendition/low-res/Content/Public', 'Autonomous weather station on East Antarctic ice', 'EurekAlert'],
  ]),
  energy: pair([
    ['https://www.antarcticstation.org/assets/ceimg_cache/assets/uploads/news_images/solar_panels_belare_2011_920_518_80_s_c1_c_c.jpg', 'Solar panels installed at an Antarctic research station', 'Princess Elisabeth Antarctica'],
    ['https://s.alicdn.com/@sc04/kf/H0bc2860a50054375881b2571f78f77b58/500kw-380v-Horizontal-Windmill-Turbine-Generators-Industrial-Wind-Electricity-Generator.jpg', 'Wind turbine generator equipment', 'Alibaba listing · illustrative equipment image'],
  ]),
  infrastructure: pair([
    ['https://www.antarctica.gov.au/site/assets/files/48848/5fb4.1200x630.jpg', 'Insulated modular Antarctic station building', 'Australian Antarctic Program'],
    ['https://www.rainews.it/dl/img/2022/12/06/1670312262039_concordia.jpg', 'Raised research modules at Concordia Station', 'Rai News'],
  ]),
  equipment: pair([
    ['https://aip.brightspotcdn.com/dims4/default/0ac991a/2147483647/strip/true/crop/574x430%2B0%2B0/resize/574x430%21/quality/90/?url=https%3A%2F%2Fk1-prod-aip.s3.us-east-2.amazonaws.com%2Fbrightspot%2FPTO.v66.i12.8_1.f1.jpg', 'Satellite equipment shelter and dish at an Antarctic ground station', 'Physics Today'],
    ['https://www.nesdis.noaa.gov/s3/styles/webp/s3/migrated/GOES_SPMGT_09-small.jpg.webp?itok=Pi-efHPQ', 'Satellite communication antenna at South Pole Station', 'NOAA NESDIS'],
  ]),
  maintenance: pair([
    ['https://www.antarctica.gov.au/site/assets/files/50364/1_-the-tractor-towing-the-two-shipping-containers_-it-was-dark-when-we-leftjpg.800x450.jpg', 'Field vehicle supporting Antarctic weather station maintenance', 'Australian Antarctic Program'],
    ['https://blogs.esa.int/concordia/files/2018/08/Antarctic-Caravan_Giorgioni_PNRA.jpg', 'Tracked vehicle and supply sleds on an Antarctic traverse', 'European Space Agency'],
  ]),
  logistics: pair([
    ['https://english.cas.cn/newsroom/archive/china_archive/cn2019/201902/W020190211319453174018.jpg', 'Tracked tractor hauling supply containers near an Antarctic station', 'Chinese Academy of Sciences'],
    ['https://blogs.esa.int/concordia/files/2018/08/Traverse-2_Giorgioni_PNRA-1024x682.jpg', 'Antarctic resupply convoy crossing the ice', 'European Space Agency'],
  ]),
  inventory: pair([
    ['https://www.nipr.ac.jp/jare/now/image60/20200121-01.jpg', 'Snow tractor moving a cargo container at Showa Station', 'National Institute of Polar Research, Japan'],
    ['https://jobs.antarctica.gov.au/site/assets/files/1889/rs79129.1200x0.jpg?nc=8387', 'Tracked vehicle carrying supplies across Antarctic snow', 'Australian Antarctic Division'],
  ]),
  alerts: pair([
    ['https://amrc.ssec.wisc.edu/aws/images/station_images/GIL_29nov2017_before.gif', 'Automatic weather station on the Antarctic ice shelf', 'University of Wisconsin AMRC'],
    ['https://www.epfl.ch/labs/cryos/wp-content/uploads/2019/08/cryos_measurement_station_East_Antarctica-1-1024x576.jpg', 'Snow and weather measurement instruments in East Antarctica', 'EPFL CRYOS'],
  ]),
  emergency: pair([
    ['https://www.antarctica.gov.au/site/assets/files/21769/insitu_gps.514x600.jpg', 'Field researchers and instruments on Antarctic ice', 'Australian Antarctic Program'],
    ['https://static.dw.com/image/38112230_702.jpg', 'Remote Antarctic satellite tracking outpost', 'Deutsche Welle'],
  ]),
  analytics: pair([
    ['https://www.mediastorehouse.com.au/p/747/blue-glacier-snow-capped-mountains-fjord-18148276.jpg.webp', 'Blue glacier and snow-covered mountain range', 'Media Storehouse'],
    ['https://imagenes.eltiempo.com/files/image_1200_600/uploads/2017/04/16/58f43323c1791.jpeg', 'Antarctic ice shelf and surrounding ocean', 'El Tiempo'],
  ]),
  reports: pair([
    ['https://www.esa.int/var/esa/storage/images/esa_multimedia/images/2025/12/esa_s_lab_at_concordia_station/27039429-1-eng-GB/ESA_s_lab_at_Concordia_station.jpg', 'Scientist working in a polar research laboratory', 'European Space Agency'],
    ['https://www.antarcticstation.org/assets/ceimg_cache/assets/uploads/pictgalleries_images/belare_20122013_firstdays_007_920_518_80_s_c1_c_c.jpg', 'Communications and power infrastructure at a polar station', 'Princess Elisabeth Antarctica'],
  ]),
  polarai: pair([
    ['https://www.windsturbine.com/photo/ps113982847-white_high_output_wind_generator_220v_70kw_whole_house_wind_turbine_kit.jpg', 'Electric generator components in an industrial workshop', 'Windsturbine.com · illustrative equipment image'],
    ['https://www.esa.int/var/esa/storage/images/esa_multimedia/images/2025/12/esa_s_lab_at_concordia_station/27039429-1-eng-GB/ESA_s_lab_at_Concordia_station.jpg', 'Researcher analyzing samples in a polar laboratory', 'European Space Agency'],
  ]),
  settings: pair([
    ['https://www.esa.int/var/esa/storage/images/esa_multimedia/images/2025/12/esa_s_lab_at_concordia_station/27039429-1-eng-GB/ESA_s_lab_at_Concordia_station.jpg', 'Antarctic laboratory equipment and instrumentation', 'European Space Agency'],
    ['https://www.coolantarctica.com/Bases/South_Pole/images/P1250012-orig.jpg', 'Communications dish and facility at the South Pole', 'Cool Antarctica'],
  ]),
};
