const express = require('express');
var sqlite3 = require('sqlite3').verbose();
const app= express();
var db = new sqlite3.Database('./Database.db3');  
app.use(express.static(__dirname + '/static'));

app.get('', (req,res) => {
    res.render('index.ejs', {
        title:null,
        content:null
    })

});

app.get('/home/:pageId', (req,res) =>{
    
    db.get('SELECT pageId, title, content FROM pages WHERE pageId='+req.params.pageId+';',function(err,rows) {
        if (err) 
        {
            res.status(500).end(" " + err)
        }
        else if(rows == undefined )
        {
            res.status(404).render('404.ejs')
        }
        else
        {
            res.render('index.ejs', {
                title:rows.title,
                content:rows.content
            })
        }
    });        
               
 });
        

app.use(function(req,res){
    res.status(404).render('404.ejs');
});

const port=process.env.PORT || 5000;

app.listen(port, "0.0.0.0", ()=> console.log(`Listening on port ${port}...!!!`));


