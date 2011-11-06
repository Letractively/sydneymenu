var filter = {LOCATION:{x:0,y:0},
                   MAIN:'',
                   STYPE:'',
                   NATION:'',
                   RADIUS:1,
                   PRICE:{MIN:40,MAX:90}
                  }

function MarkInvalidate(str){
  YUI().use("node",function(Y){
    ele = Y.one("div.invalid-hint");
    if(str){
      ele.set("innerHTML",str);
      ele.setStyle("display","block");
    }
  });
}
function MarkValidate(){
  YUI().use("node",function(Y){
    Y.one("div.invalid-hint").setStyle("display","none");
  });
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
      var patten = new RegExp("[a-zA-Z]+");
      if(patten.test(searchStr)){
        MarkValidate();
      }else{
        MarkInvalidate("Invalid Query String");
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
     var search_option = Y.one("#match-option");
     zoyoe.search = InitSearch(search_option,"/address");
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

function InitSearch(opt_ele_container,option_path){
  var search = new function(){
    var self = this;
    this.option = option_path;
    this.optcontainer = opt_ele_container;
    this.SetPreference = function(path,idx){
      self.optcontainer.all('a').set('className','');
      self.optcontainer.all('a').item(idx).set('className','select');
    }
    this.SearchByAddress = function(){
    YUI().use("json-stringify","node",function (Y) {
      var searchStr = Y.Node.getDOMNode(Y.one("#search-bar input")).value;
      var patten = new RegExp("[a-zA-Z]+");
      if(patten.test(searchStr) == false){
        MarkInvalidate("Invalid Query String");
        return;/* early return here, since the search string is empty */
      }
      searchStr = refineAddress(searchStr);
      filter.STYPE = NonePadding(Y.Node.getDOMNode(Y.one("#service-type input")).value);
      filter.NATION = NonePadding(Y.Node.getDOMNode(Y.one("#nationality input")).value);
      var radius_str = Y.Node.getDOMNode(Y.one("#radius input")).value;
      filter.RADIUS = NonePadding(parseInt(radius_str));
      filter.PRICE.MIN = NonePadding(document.forms['search'].min.value);
      filter.PRICE.MAX = NonePadding(document.forms['search'].max.value);
      var filterStr = Y.JSON.stringify(filter);
      zoyoe.ALERT(searchStr);
      zoyoe.map.TargetPlace(searchStr,"Search")
    });
    }
  };
  return search;
}


function Search(result){
  if(result && result.resourceSets){
    if(result.resourceSets[0].estimatedTotal = 0){
      MarkInvalidate('Address Not Found !!');
    }
    else if(result.resourceSets[0].estimatedTotal = 1){
      var resources = result.resourceSets[0].resources;
      if(resources.length == 0){
        MarkInvalidate('Address Not Found !!');
      }else if(resources.length == 1){
        zoyoe.ALERT(resources[0].address.formattedAddress);
        var c = resources[0].point.coordinates;
        zoyoe.ALERT(c);
        filter.LOCATION.x = c[0];
        filter.LOCATION.y = c[1];
        YUI().use("json-stringify","node",function (Y) {
          var filterStr = Y.JSON.stringify(filter);
          var searchStr = Y.Node.getDOMNode(Y.one("#search-bar input")).value;
          window.location.href = "/core/services/?"+"filter=" + filterStr;
        });
      }else{
        MarkInvalidate("Ambiguious Address, Please Make It Clear !!");
      }
    }
    else{
      MarkInvalidate('Multi Address Found,Please Make It Clear !!');
    }
  }
}

