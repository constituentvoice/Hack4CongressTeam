module.exports = function(Question) {
  var app, _;
  app = require('../../server/server');
  _ = require('underscore');
  Question.stats = function(id, cb) {
    var q;
    return q = Question.find({
      where: {
        id: id
      },
      include: ['responses']
    }, function(err, question) {
      var commentPct, commentTotal, nTotal, percent, yTotal;
      if (err) {
        throw err;
      }
      yTotal = 0;
      nTotal = 0;
      commentTotal = 0;
      question = question[0];
      _.each(question.responses(), function(response) {
        console.log(response.text);
        if (response.text === 'y') {
          return yTotal = yTotal + 1;
        } else if (response.text === 'n') {
          return nTotal = nTotal + 1;
        } else {
          return commentTotal = commentTotal + 1;
        }
      });
      console.log(yTotal);
      console.log(nTotal);
      console.log(commentTotal);
      percent = yTotal / (yTotal + nTotal);
      percent = Math.round(percent * 100) / 100;
      commentPct = Math.round((commentTotal / (yTotal + nTotal + commentTotal)) * 100) / 100;
      return cb(null, {
        "percent": percent,
        "commentPercent": commentPct
      });
    });
  };
  return Question.remoteMethod("stats", {
    accepts: [
      {
        arg: 'id',
        type: 'string',
        required: true
      }
    ],
    http: {
      path: '/:id/stats',
      verb: 'get'
    },
    returns: {
      root: true
    }
  });
};
