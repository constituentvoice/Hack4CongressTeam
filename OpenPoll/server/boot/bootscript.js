module.exports = function(app) {
  app.dataSources.sql.automigrate(function(err) {});
  return console.log("end boot");
};
