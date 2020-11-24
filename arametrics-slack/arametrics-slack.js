"use strict";
// Author        : Aravinth Panch
// Description   : Map SLACK Users JSON to flat CSV for export"

const fs = require("fs");
const {convertArrayToCSV} = require("convert-array-to-csv");

let raw_data_files = ["data/2020-11-24.json"];
const csv_header = [
  "real_name",
  "display_name",
  "title",
  "username",
  "email",
  "image_original"
];
let users_array = [];
let users_csv = [];

// Extract from all the files
raw_data_files.forEach((raw_data_file) => {
  // Read the json file and get items
  let raw_data = fs.readFileSync(raw_data_file);
  let users_json = JSON.parse(raw_data).members;

  // Cherypick needed fields
  users_json.forEach((item) => {
    let user = [
      item.profile.real_name,
      item.profile.display_name,
      item.profile.title,
      item.username,
      item.profile.email,
      item.profile.image_original
    ];
    if (item.is_bot == false)
      users_array.push(user);
    }
  );

  // Convert the users data to CSV format
  users_csv = convertArrayToCSV(users_array, {
    header: csv_header,
    separator: ","
  });
});

// Save the CSV data to the CSV file
console.log(users_csv);
fs.writeFile("data/output.csv", users_csv, function(err) {
  if (err)
    return console.log(err);
  console.log("Done !!!");
});
