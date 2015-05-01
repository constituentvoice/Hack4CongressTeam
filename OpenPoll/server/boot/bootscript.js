module.exports = function(app) {
  var rebootDB;
  rebootDB = false;
  if (rebootDB) {
    app.dataSources.mySQL.automigrate(function(err) {});
  }
  return console.log("end boot");
};
