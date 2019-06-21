let {PythonShell} = require('python-shell')
var path = require("path")
let dialog = require('electron').remote.dialog
var file_path;
var Image_path;

function get_csv_path(img){
  file_path = dialog.showOpenDialog()[0]
  if(img){
    document.getElementById("csv-file").setAttribute("src",img);
    console.log(img);
  }
}

function get_image_path(){
  Image_path = dialog.showOpenDialog()[0]
  if(Image_path){
    document.getElementById("answer-image").setAttribute("src",Image_path);
  }
}


function get_score() {

  var options = {
    mode: 'text',
    scriptPath : path.join(__dirname, '/../engine/'),
    args : [file_path, Image_path]
  }
  console.log("pavan")
  PythonShell.run('omr.py', options, function (err, result){
    if(err) throw err;
    alert(result[1]);
  });
  
  document.getElementById("csv-file").setAttribute("src","");
  document.getElementById("answer-image").setAttribute("src","");
}
