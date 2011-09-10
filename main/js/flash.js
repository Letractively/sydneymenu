/*function that get the flash component*/   
function getFComp(movieName) {
 if (navigator.appName.indexOf("Microsoft") != -1) {
   return document.getElementById('ie_'+movieName);
   //return window[movieName];
 } else {
   if(document[movieName]){
     return document[movieName];
   }
   else{
     return document.getElementById(movieName);
   }
 }
}
function SetUploader(sname){
  var uploader = getFComp('uploader');
  uploader.AddEventHandler('Select','SelectHandler');
  uploader.AddEventHandler('Progress','ProgressHandler');
  uploader.AddEventHandler('Complete','CompleteHandler');
  uploader.AddEventHandler('Complete','CompleteHandler');
  uploader.AddEventHandler('IOError','ErrorHandler');
  uploader.SetUrl("http://"+window.location.host+"/core/imagecache/"+sname+"/cache/");
  //alert (uploader.Status());
}
