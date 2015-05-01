module.exports = (app) ->
    rebootDB = false

    if rebootDB
        app.dataSources.mySQL.automigrate((err) ->

        )
    
    console.log("end boot")