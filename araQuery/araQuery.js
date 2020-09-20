// Author        : Aravinth Panch
// Description   : Map SLACK Users JSON to flat CSV for export"


var jsonQuery = require('json-query')

var data = {
  people: [
    {name: 'Matt', country: 'NZ'},
    {name: 'Pete', country: 'AU'},
    {name: 'Mikey', country: 'NZ'}
  ]
}

var res = jsonQuery('people[country=NZ].name', {
  data: data
});

console.log(res.value)
