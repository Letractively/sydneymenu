var filter = {LOCATION:{x:0,y:0},
                   STYPE:'Brothel',
                   NATION:'Caucasion',
                   RADIUS:1,
                   PRICE:{MIN:40,MAX:90}
                  }

function document_load(){
  zoyoe.map = new MapInfoCore(function(){},null,null,null);
  if(zoyoe.ElementExtension){
    zoyoe.ElementExtension.BuildExtensionElements();
  }
  YUI().use("node",function(Y){
     var input = Y.one("div.extension-auto-complete").one("input");
     var dom_input = Y.Node.getDOMNode(input);
     dom_input.ext_onchange = function(searchStr){
       if(zoyoe.map){
          zoyoe.map.TargetPlace(searchStr,"AutoCompJSON");
       } else {
       zoyoe.ALERT("Map not loaded");
       }
     }
     var types = Y.one("#restaurant-type");
     type_html = "";
     for (var key in zoyoe.restaurant_type){
       var tlist = zoyoe.restaurant_type[key];
       for(var i = 0;i<tlist.length;i++){
         type_html +="<li>" + tlist[i] + "</li>"; 
       }
     }
     types.set("innerHTML","<ul>"+type_html+"</ul>");
  });
}
function Search(result){
  if(result && result.resourceSets){
    if(result.resourceSets[0].estimatedTotal = 0){
      zoyoe.ALERT('Address Not Found !!');
    }
    else if(result.resourceSets[0].estimatedTotal = 1){
      var resources = result.resourceSets[0].resources;
      if(resources.length == 0){
        zoyoe.ALERT('Address Not Found !!');
      }else if(resources.length == 1){
        zoyoe.ALERT(resources[0].address.formattedAddress);
        var c = resources[0].point.coordinates;
        zoyoe.ALERT(c);
        filter.LOCATION.x = c[0];
        filter.LOCATION.y = c[1];
      }else{
        zoyoe.ALERT("Ambiguious Address, Please Make It Clear !!");
      }
    }
    else{
      zoyoe.ALERT('Multi Address Found,Please Make It Clear !!');
    }
  }
  YUI().use("json-stringify","node",function (Y) {
    var filterStr = Y.JSON.stringify(filter);
    var searchStr = Y.Node.getDOMNode(Y.one("#search-bar input")).value;
    window.location.href = "/core/services/?"+"filter=" + filterStr;
  });
}

function NonePadding(str){
  if(str){return str;}
  else{return "";}
}

function refineAddress(address){
  address = doRefine(address, ", Australia");
  address = doRefine(address, ",Australia");
  address = doRefine(address, ", NSW");
  address = doRefine(address, ",NSW");
  return address;
}

function doRefine(address, refiner) {
  if(address.indexOf(refiner) != -1) {
    address = address.replace(refiner, "");
  }
  return address;
}

function PreSearch(){
  YUI().use("json-stringify","node",function (Y) {
    var searchStr = Y.Node.getDOMNode(Y.one("#search-bar input")).value;
      searchStr = refineAddress(searchStr);
    filter.STYPE = NonePadding(Y.Node.getDOMNode(Y.one("#service-type input")).value);
    filter.NATION = NonePadding(Y.Node.getDOMNode(Y.one("#nationality input")).value);
    var radius_str = Y.Node.getDOMNode(Y.one("#radius input")).value;
    filter.RADIUS = NonePadding(parseInt(radius_str));
    filter.PRICE.MIN = NonePadding(document.forms['search'].min.value);
    filter.PRICE.MAX = NonePadding(document.forms['search'].max.value);
    var filterStr = Y.JSON.stringify(filter);
    if(searchStr == ""){
      var filterStr = Y.JSON.stringify(filter);
      filter.LOCATION.x = 0;
      filter.LOCATION.y = 0;
      window.location.href = "/core/services/?"+"filter=" + filterStr;
    }
    zoyoe.ALERT(searchStr);
    zoyoe.map.TargetPlace(searchStr,"Search")
  });
}
