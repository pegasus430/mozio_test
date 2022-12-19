# Mozio api test
 - Built a JSON REST API with CRUD operations for Provider (name, email, phone number, language an currency) and ServiceArea (name, price, geojson information)

 - Created a specific endpoint that takes a lat/lng pair as arguments and return a list of all polygons that include the given lat/lng. The name of the polygon, provider's name, and price should be returned for each polygon

## standard api endpoint
### swagger 
```bash
http://ec2-15-222-8-181.ca-central-1.compute.amazonaws.com:8000/swagger
```

### API 

```bash

http://ec2-15-222-8-181.ca-central-1.compute.amazonaws.com:8000/api/providers
http://ec2-15-222-8-181.ca-central-1.compute.amazonaws.com:8000/api/servicearea
http://ec2-15-222-8-181.ca-central-1.compute.amazonaws.com:8000/getpolygons/?lat={lat_value}&lng={lng_value}
```
## standard service area format
```bash
{
   "name": "serviceare1",
   "price": 3332.99,
   "geoJson": {
       "type": "Polygon",
       "coordinates": [
           [
               100.0,
               0.0
           ],
           [
               101.0,
               0.0
           ],
           [
               101.0,
               1.0
           ],
           [
               100.0,
               1.0
           ],
           [
               100.0,
               0.0
           ]
       ],
       "provider": "provider1"
   }
}
```
## standard provider format
```bash
{
    "name": "provider1",
    "email": "provider1@test.com",
    "phoneNumber": "3524569542",
    "language": "ENG",
    "currency": "USD",
}
```