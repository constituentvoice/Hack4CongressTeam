module.exports = function(app) {
  app.dataSources.mySQL.automigrate(function(err) {});
  return console.log("end boot");
};
