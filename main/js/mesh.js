function BuildPoint(x,y){
  return new Microsoft.Maps.Location(x, y);
}

function Service(element){
  this.type = element.getAttribute("type");
  this.name = element.getAttribute("name");
  this.email= element.getAttribute("email");
  this.phone= element.getAttribute("phone");
  this.grade = element.getAttribute("grade");
  this.privilege= element.getAttribute("privilege");
  this.activity= element.getAttribute("activity");
  this.icon= element.getAttribute("icon");
  this.address =  element.getElementsByTagName("address")[0].firstChild.data;
  this.description = element.getElementsByTagName("description")[0].firstChild.data;
  var loc_string = element.getElementsByTagName("latlong")[0].firstChild.data.split(",",2);
  this.loc = BuildPoint(parseFloat(loc_string[0])/1000000,parseFloat(loc_string[1])/1000000);
  this.days = {}
  this.in_square = false;
  var working_days = element.getElementsByTagName("days")[0].firstChild.data.split(',');
  for(var i=0;i<working_days.length;i++){
     this.days[working_days[i]] = true;   
  }
  this.active = true;
  this.WorkingDaysStr = function(){
    var ret = [];
    var ds = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
    for(var i=0;i<ds.length;i++){
      if(this.days[ds[i]]){
        ret.push(ds[i]);
      }
    }
    return ret.join(','); 
  }
}

function ServiceReport(element){
  this.type = "Report";
  this.name = element.getAttribute("name");
  this.dishtype = element.getAttribute("type");
  this.who = element.getAttribute("who");
  this.address =  element.getElementsByTagName("address")[0].firstChild.data;
  var loc_string = element.getElementsByTagName("latlong")[0].firstChild.data.split(",",2);
  this.loc = BuildPoint(parseFloat(loc_string[0])/1000000,parseFloat(loc_string[1])/1000000);
  this.active = true;
}

function AgeFilter(low,high){
    this.low = low;
    this.high = high;
    this.filt = function (service){
      return true;
      if (service.age.high >= this.low && service.age.low <= this.high){
        return true;
      }else{
        return false;
      }
    }
}
function WorkingDayFilter(){
  this.slots = {'Mon':true,'Tue':true,'Wed':true,'Thu':true,'Fri':true,'Sat':true,'Sun':true};
  this.keys = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
  this.filt = function (service){
    if(service.type == "Report"){
      return true;
    }else{
      for(var i=0;i<this.keys.length;i++){
        if(this.slots[this.keys[i]] && service.days[this.keys[i]]){
          return true
        }
      }
    }
    return false;
  }
}
function TypeFilter(){
  this.check = {'mixed':true,'Shop':true,'Report':true}
  this.filt = function(service){
    var type = service.type;
    if(type != "Report"){
       type = "Shop"
    }
    if(this.check[type] == true){
      return true;
    }else{
      return false;
    }
  } 
}
function RearrangeEvents(map_core){
  var this_map=map_core.map;
  var core = map_core;
  Microsoft.Maps.Events.addHandler(this_map,'viewchangeend',
    function(event){
        core.ShiftZoom();
        var fa = GetMapArea();
        var groups = core.GetServicesInSquare(fa.left,fa.top,fa.width,fa.height);
        if(map_core.disable_handler != true){
          RefreshServicesInRightDock(groups);
        }
    });
  Microsoft.Maps.Events.addHandler(this_map,'viewchangestart',
    function(event){
      var zoom = core.map.getTargetZoom();
      if (zoom > 16){
        core.map.setView({'zoom':16,'animate':false})
      }
      return true;
    });
}
function filt(service,filters){
  var filter_idx = 0;
  for(;filter_idx<filters.length;filter_idx++){
    if(! filters[filter_idx].filt(service)){return false}
  }
  return true;
}
function TargetPlaceJSON(result){
  if(result.resourceSets){
    if(result.resourceSets[0].estimatedTotal = 0){
      zoyoe.ALERT('Address Not Found !!');
    }
    else if(result.resourceSets[0].estimatedTotal = 1){
      var resources = result.resourceSets[0].resources;
      if(resources.length == 0){
        BuildErrorMsg('Address Not Found !!');
      }else if(resources.length == 1){
        zoyoe.ALERT(resources[0].address.formattedAddress);
        var c = resources[0].point.coordinates;
        zoyoe.ALERT(c);
        zoyoe.map.map.setView({center:new Microsoft.Maps.Location(c[0],c[1])});
      }else{
        zoyoe.ALERT("Ambiguious Address, Please Make It Clear !!");
      }
    }
    else{
      zoyoe.ALERT('Multi Address Found,Please Make It Clear !!');
    }
  }
}
function ServiceGeoGroup(service){
  var self = this;
  this.loc = service.loc;
  this.service_list = new Array();
  this.report_list = new Array();
  this.pushpin = new Microsoft.Maps.Pushpin(this.loc,{anchor:{x:15,y:15},height:30,width:30});
  this.mouseover = Microsoft.Maps.Events.addHandler(this.pushpin,'click',
    function(e){
      if(zoyoe){
	      var gp = zoyoe.map.map.tryLocationToPixel(self.loc,Microsoft.Maps.PixelReference.page);
            zoyoe.ShowShortCut(gp,self.service_list,self.report_list);
      }
    });
  this.BuildIcon = function(ctr){
    var s_count = 0;
    var r_count = 0;
    for(var i=0;i<this.service_list.length;i++){
      if(this.service_list[i].active){
        s_count++;
      }
    } 
    for(var i=0;i<this.report_list.length;i++){
      if(this.report_list[i].active){
        r_count++;
      }
    } 
   var act_pin = null;
   var inact_pin = null; 
   if(r_count !=0 && s_count ==0){
      act_pin = "/res/pushpin/burger.png";
      inact_pin = "/res/pushpin/burger_inactive.png";
    }else{
      act_pin = "/res/pushpin/pushpin.png";
      inact_pin = "/res/pushpin/pushpin_inactive.png";
    }
    if(s_count>0){
      this.pushpin.setOptions({icon:act_pin,text:''+s_count});
    }else if(r_count>0){
      this.pushpin.setOptions({icon:act_pin,text:''+r_count});
    }else{
      this.pushpin.setOptions({icon:inact_pin,text:'?'});
    }
  }
  this.Absorb = function(service){
    var weight = this.service_list.length;
    if (service.type != "Report"){
		  this.service_list.push(service);
    }else{
		  this.report_list.push(service);
    }
		this.BuildIcon(false);
  }
  this.Absorb(service);
}
function Layer(){
	this.geo_service_group = new Array();
	this.layer = null;
	this.status = "not_ready";
  this.BuildIcons = function(){
    for(var i=0;i<this.geo_service_group.length;i++){
      this.geo_service_group[i].BuildIcon(true);
    }
  }
  this.Show = function(){
    this.layer.setOptions({visible:true});
  }
  this.Hide = function(){
    this.layer.setOptions({visible:false});
  }
}

function MapInfoCore(callback,address,container_id,zoom,disable_handler){
/* Safe self reference */
  var self = this;
  var age_filter_idx = 0;
  var workingday_filter_idx = 1;
  var type_filter_idx = 2;
  this.container_id = container_id;
  this.insertedChild = null;
  this.current_zoom = null;
  this.push_pin_id = 0;
  this.general_map_zoom = 16;
  this.pushpin_layers = new Array();
  this.disable_handler = disable_handler;
  for(var i=0;i<20;i++){
    this.pushpin_layers[i] = new Layer();
  }
  this.services_cache = new Array();

/* All Filter Reset functions*/
  this.filterlist = new Array(new AgeFilter(16,45),new WorkingDayFilter(),new TypeFilter());

  this.ResetAgeFilter = function (low,high){
    if(high<low){high = low;alert('error');}
    this.filterlist[age_filter_idx].low = low;
    this.filterlist[age_filter_idx].high = high;
    this.Refilt();
  }
  this.ToggleWorkingDayFilter = function(dstr){
    var c = this.filterlist[workingday_filter_idx].slots[dstr]; 
    this.filterlist[workingday_filter_idx].slots[dstr] = (c == true) ? false:true;
    this.Refilt();
  }
  this.ToggleTypeFilter = function(dstr){
    var c = this.filterlist[type_filter_idx];
    if(c.check[dstr] != undefined){
      if(c.check[dstr]){
        c.check[dstr] = false;
      }else{
        c.check[dstr] = true;
      }
    }
    this.Refilt();
  }
  if(address){
    this.default_address_point = address;
  }else{
    this.default_address_point = new Microsoft.Maps.Location(-33.882416032, 151.179791973);
  }
  if(zoom){
    this.default_zoom = zoom;
  }else{
    this.default_zoom = 12;
  }


/* Not used now, Leave here to see what happened */
  this.current_services = new Array();
  this.current_push_pins = new Array();

  this.AddService = function(service){
    this.services_cache.push(service);
  }
/* Check whether a service is near a group or not */
	this.NeighbourAtCurrentZoom = function(group,service){
    var gp = this.map.tryLocationToPixel(group.loc,Microsoft.Maps.PixelReference.page);
    var sp = this.map.tryLocationToPixel(service.loc,Microsoft.Maps.PixelReference.page);
    return (Math.abs(gp.x-sp.x)<=15&&Math.abs(gp.y-sp.y)<=15);
	}
  
 this.TargetPlace = function(where,cbname){
    var script = document.createElement("script");
    script.setAttribute("type","text/javascript"); 
    script.setAttribute("src",this.SearchUri(where+' ,NSW ,Australia')+"&jsonp="+cbname);
    if(this.insertedChild != null) {
      document.body.removeChild(this.insertedChild);
    }
    this.insertedChild = document.body.appendChild(script);
	}
  /* Always use the current function to get the current layer */
  this.GetCurrentLayer = function(){
		var layer_id = this.map.getZoom();
		if(layer_id >= 20){
			return null;// Should never go here;
		}else if(this.pushpin_layers[layer_id].filled == true){
      return this.pushpin_layers[layer_id];
    }else{
      return null;// Should never go here;
    }
  }
  this.GetServicesInSquare = function(left,top,width,height){
		for(idx = 0;idx < self.services_cache.length;idx++){
		 var service = self.services_cache[idx];
     service.in_square = false;
    }
    var pdx = 0;
    var groups= new Array();
    var layer = this.GetCurrentLayer();
    if (layer == null){
      return groups; /*Should never go here */
    }
    for(pdx = 0;pdx <layer.geo_service_group.length;pdx++){
      var service_group = layer.geo_service_group[pdx];
      var gp = this.map.tryLocationToPixel(service_group.loc,Microsoft.Maps.PixelReference.page);
      if(gp.x>=left&&gp.x<=left+width&&gp.y>=top&&gp.y<=top+height){
        groups.push(service_group);
      }
    }
    return groups;
  }
	this.AbsorbService = function(service){
		var layer_id = this.map.getZoom();
		if(layer_id >= 20){
			return false;
		}else if(this.pushpin_layers[layer_id].filled == true){
			return false;
		}else{
			var layer = this.pushpin_layers[layer_id];
			if(layer.layer == null){
				layer.layer = new VEShapeLayer();
			}
			var pdx = 0;
			for(pdx = 0;pdx <layer.geo_service_group.length;pdx++){
				var service_group = layer.geo_service_group[pdx]
				if(this.NeighbourAtCurrentZoom(service_group,service)){
					service_group.Absorb(service);
					break;
				}
			}
			if(pdx == layer.geo_service_group.length){
				var group = new ServiceGeoGroup(service);
				layer.geo_service_group.push(group);
				layer.layer.push(group.pushpin);
			}
		}
	}
	this.InitServices = function(){
		var layer_id = this.map.getZoom();
		if(layer_id >= 20){
			return false;
		}else if(this.pushpin_layers[layer_id].filled == true){
			return false;
		}else{
		  var idx = 0;
		  for(idx = 0;idx < self.services_cache.length;idx++){
			  var service = self.services_cache[idx];
			  self.AbsorbService(service);
		  }
      this.pushpin_layers[layer_id].filled = true;
      this.Refilt();
    }
	}
	this.PreviewService = function(service){
	}
	this.ShiftZoom = function(force){
		var zoom = this.map.getZoom();
    if (zoom != self.current_zoom || force){
		  if (self.current_zoom !=null){
			  if (self.pushpin_layers[self.current_zoom] !=null){
				  var layer = self.pushpin_layers[self.current_zoom];
				  if(layer.status == 'ready'){
					  layer.Hide();
				  }
			  }
		  }
		  if(this.pushpin_layers[zoom] !=null){
			  var layer = this.pushpin_layers[zoom];
        layer.BuildIcons();
			  if(layer.status == 'ready'){
				  layer.Show();
			  }else{
				  this.InitServices();
				  layer.status = 'ready';
				  layer.Show();
			  }
		  }else{alert("not_supported:"+zoom);}
		  self.current_zoom = zoom;
    }else{
    }
	}
  this.key = "Av6myMPPl0Aix9wsk-YXGQ23bvY1A3I2dmHJ44GAVYwlF_70J4OJdmv_SqM1rFJd";
  this.map_options = {credentials:this.key,showDashboard:false,mapTypeId:Microsoft.Maps.MapTypeId.road
  ,disableUserInput:false,showCopyright:false,showScalebar:false
  ,enableSearchLogo:false,enableSearchLogo:false
  ,zoom:this.default_zoom,center:this.default_address_point}
  if(disable_handler){
    this.map_options.disableUserInput = true;
  }
  this.current_zoom = this.default_zoom;
  this.search_prefix = "http://ecn.dev.virtualearth.net/REST/v1/Locations?key="
                      + this.key + "&query="
  this.SearchUri = function(address){
    return this.search_prefix + address;
  }
  function init_layers(){
    var the_map = self.map;
    RearrangeEvents(self);
    for(var i=0;i<20;i++){
        self.pushpin_layers[i].layer = new Microsoft.Maps.EntityCollection({visible:true});
        self.map.entities.push(self.pushpin_layers[i].layer);
    }
    callback(self);
  }
  this.Refilt = function(){
    for(idx = 0;idx < self.services_cache.length;idx++){
      var service = self.services_cache[idx];
      if(filt(service,self.filterlist)){
        service.active = true;
      }else{
        service.active = false;
      }
    }
		var zoom = this.map.getZoom();
    if(this.pushpin_layers[zoom]){
      this.pushpin_layers[zoom].BuildIcons();
    }
  }
  if(container_id){
    this.map = new Microsoft.Maps.Map(document.getElementById(container_id),this.map_options);
    init_layers();
  }
}


