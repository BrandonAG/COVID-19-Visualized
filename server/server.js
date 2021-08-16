const path = require('path');
const express = require('express');

const PORT = process.env.PORT || 3001;
const app = express();


app.use(express.urlencoded({ extended: false }));
app.use(express.json());

// Serve up static assets
if (process.env.NODE_ENV === 'production') {
  app.use(express.static(path.join(__dirname, '../client/build')));
}

app.get('/api/today', (req,res) => {
    res.sendFile(path.join(__dirname,'_tmp/tmp.json'))
})
app.get('/', (req,res) => {
    res.sendFile(path.join(__dirname,'_tmp/tmp.json'))
})
// app.get('*', (req, res) => {
//   res.sendFile(path.join(__dirname, '../client/build/index.html'));
// });

// db.once('open', () => {
  app.listen(PORT, () => {
    console.log(`API server running on port ${PORT}!`);
    // log where we can go to test our GQL API
    // console.log(`Use GraphQL at http://localhost:${PORT}`);
  });
// });