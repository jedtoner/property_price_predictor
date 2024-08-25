Data:
 - House data (bed, bath, park, sq footage) - obtained from Kaggle (done)
 - Macroeconomic data (maybe use kaggle provided)
 - Geolocation data - distance to various amenities (cbd, schools, parks, shops)
  - https://openrouteservice.org/plans/ (driving/walking)
  - https://project-osrm.org/ (driving/walking)
  - https://www.interline.io/transitland/apis-for-developers/ (PT)
  - openstreetmaps (parks)

 - Historic prices / renovations / year built
 - View
 - Busy road / train factor
 - Amenities (solar panels, heating)
 - Neighbourhood quality (crime rates, school quality)
  - https://www.dva.gov.au/sites/default/files/Providers/nsworp.pdf Suburb to postcode
  - https://docs.google.com/spreadsheets/d/1tHCxouhyM4edDvF60VG7nzs5QxID3ADwr3DGJh71qFg/edit?gid=900781287#gid=900781287 postcode to LGA

 Considerations:
  - Sq footage not always available

TODO:
  - Use code at bottom of file to read suburb to postcode pdf (move tabula to req.txt)
  - Improve suburb to LGA workflow
  - Look at 'suburb rankings' to infer neighbourhood quality