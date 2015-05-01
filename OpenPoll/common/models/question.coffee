module.exports = (Question) ->
    app = require('../../server/server')
    _ = require('underscore')
    
    Question.stats = (id, cb)->
        q = Question.find(
            where:
                id: id
            include: ['responses']
        , (err, question)->
            throw err if err
            yTotal = 0
            nTotal = 0
            commentTotal = 0
            question = question[0]
            _.each(question.responses(), (response)->
                console.log(response.text)
                if response.text == 'y'
                    yTotal = yTotal + 1
                else if response.text == 'n'
                    nTotal = nTotal + 1
                else
                    commentTotal = commentTotal + 1
            )
            console.log(yTotal)
            console.log(nTotal)
            console.log(commentTotal)
            percent = yTotal / (yTotal + nTotal)
            percent = Math.round(percent * 100) / 100
            commentPct = Math.round((commentTotal / (yTotal + nTotal + commentTotal)) * 100) / 100
            
            cb(null, {"percent": percent, "commentPercent": commentPct})
            
        
        )
    
    
    Question.remoteMethod("stats",
        accepts: [{arg: 'id', type: 'string', required: true}]
        http: {path: '/:id/stats', verb: 'get'}
        returns: {root: true}
    )