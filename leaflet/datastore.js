firebase.initializeApp({
  apiKey: 'AIzaSyAxdD_kwzI1_8KQfqIZgouxEXjJlrrO0uE',
  authDomain: 'gis-editor-viewer.firebaseapp.com',
  projectId: 'gis-editor-viewer'
});

// Initialize Cloud Firestore through Firebase
var db = firebase.firestore();
const settings = {timestampsInSnapshots: true};
db.settings(settings);