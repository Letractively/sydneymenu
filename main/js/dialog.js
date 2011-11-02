/* The dialog.js is independent and need polish some how later */
/* The implementation need some convention in html design, so just internal use only */
/* The implementation does not use css path to find elements, it depends on the function getElementById */

/* Current Is The Main Object That We Provide For All Of Our Pages */
var zoyoe = new function(){
  this.debug = false;
  this.InitZoyoe = function(dbg,yui,static_dialog){
    this.debug = dbg;
    this.ui = new ZOYOE_UI(this,yui,static_dialog);
  }
  /* Only This Kind Of Variables Are Public */
  this.dock_style = 'ICON';
  /* Dialog Related Global Variables */
  this.comps = {};
  this.map = null;
  this.week_day = new function(){
    this.Monday=0;
    this.Tuesday=1;
    this.Wednesday=2;
    this.Thursday=3;
    this.Friday=4;
    this.Saturday=5;
    this.Sunday=6;
  }
  this.ALERT = function(str){
    if (this.debug){
      alert(str);
    }
  }
  this.Redirect =function(url){
    window.location.href = url;
  }
  this.TimeStamp = function(){
    var tstamp = "";
    if(this.timestamp){
      tstamp = "&tstamp="+this.timestamp;
    }
    return tstamp;
  }
  this.Update = function(update){
    var self = this;
    var config = {
        method: 'GET',
    }
    YUI().use("io-form",function(Y){
      function complete(id,o,args){
        zoyoe.ALERT(o.responseText);
        document.getElementById(args[0]).parentNode.innerHTML = o.responseText;
      }
      Y.on('io:complete',complete,Y,[update.comp_id]);
      var request = Y.io(update.uri,config);
    });
  }
  this.GeneralDialogInPanel = function (uri,config,cb){
    /* You must make sure the pannel is showd before calling this */
    YUI().use("io-form",function(Y){
      function complete(id,o,args){
        zoyoe.ALERT(o.responseText);
        YUI().use('node',function(yui_node){
          var panel = yui_node.one('#panel .panel-content');
          panel.set('innerHTML',o.responseText);
        });
      }
      Y.on('io:complete',complete);
      var request = Y.io(uri,config);
   });
  } 
  this.ShowShortCut = function(pos,slist,rlist){
    if(slist !=0){
      var float_info = document.getElementById('float-info');
      float_info.rotate = 0;
      var width = document.getElementById('map-info').offsetWidth - 230;
      var height = document.getElementById('map-info').offsetHeight;
      var lr = (width - pos.x)/width;
      var tb = (height - pos.y)/height;
      /* Using interpolation here */
      float_info.style.left = n2px(pos.x - 300*(1 - lr));
      float_info.style.top = n2px(pos.y - 280*(1-tb)+tb*120);
      if(this.ui.content_active){
        this.ui.HibernateContent();
        var count = 1;
        var serv = null;
        YUI().use('node',function(yui_node){
          for(var i=0;i<slist.length&&count<=4;i++){
            serv = slist[i];
            var name = serv.name; 
            var img_src = "/core/data/res/" + name + "/icon/?sc=mid";
            var img_cont = yui_node.one("#float-info div.left div.img"+count);
            img_cont.set('innerHTML',"<a class='img' href='/core/service/" + name + "/'><img src = '" + img_src +"' ></img></a>");
            count++;
          }
          for(var i=count;i<=4;i++){
            var img_cont = yui_node.one("#float-info div.left div.img"+i);
            img_cont.set('innerHTML',"");
          } 
          serv = slist[0];
          yui_node.one("#float-info .name").set('innerHTML',serv.name + " [active:" + serv.activity + "]");
          yui_node.one("#float-info .phone").set('innerHTML',serv.phone);
          yui_node.one("#float-info .email").set('innerHTML',serv.email);
          yui_node.one("#float-info .address").set('innerHTML',serv.address);
          yui_node.one("#float-info .wds").set('innerHTML',serv.WorkingDaysStr());
          yui_node.one("#float-info .description").set('innerHTML',serv.description);
          yui_node.one("#float-info .nest span").set('innerHTML',slist.length);
          var float_sh = yui_node.one('#float-info .div-scroll div.hscroll');
          var float_sh_ele = yui_node.Node.getDOMNode(float_sh);
          float_sh_ele.Reset();
          float_info.style.display = "block";
        });
      }
    }else{
    }
  }
  this.CloseShortCut = function(){
    var float_info = document.getElementById('float-info');
    float_info.style.display = "none";
    this.ui.ActivateContent();
  }
  this.HideShortCut = function(){
    this.ui.ActivateContent();
    YUI().use('node',function(yui_node){
      var float_info = node.one("#float-info");
      alert("float_find");
    });
  }
  this.SwitchDockStyle = function(style){
    this.dock_style = style;
    if(this.map){
	    var this_map= this.map.map;
	    var core = this.map;
      var fa = GetMapArea();
      var groups = core.GetServicesInSquare(fa.left,fa.top,fa.width,fa.height);
      RefreshServicesInRightDock(groups);
    }
  }
}

  
/* The following function need YUI3 to succeed */

  var config = new function(){
     this.choice = new Array();
     this.choice.push(new function(){
       this.name = 'sort-select';
       this.handler = function(type){
       }
     });
     this.combo = new Array();
     this.combo.push(new function(){
       this.name = "working-days";
       this.handler = function(type){
         zoyoe.map.ToggleWorkingDayFilter(type);
       }
     });
     this.combo.push(new function(){
       this.name = "type-select";
       this.handler = function(type){
         zoyoe.map.ToggleTypeFilter(type);
       }
     });
  }

function InitChoiceControl(setting){ 
   YUI().use('node',function(node){
     var values = node.all('#'+ setting.name + " a");
     values.on('click', function(e){
        values.removeClass('selected');
        e.currentTarget.addClass('selected');
        setting.handler(node.Node.getDOMNode(e.currentTarget.one('span')).nextSibling.data);
      });
   });
}

function InitComboControl(setting){ 
   YUI().use('node',function(node){
     var values = node.all('#'+ setting.name + " a");
     values.on('click', function(e){
        if(e.currentTarget.hasClass('selected')){
          e.currentTarget.removeClass('selected');
        }else{
          e.currentTarget.addClass('selected');
        }
        setting.handler(node.Node.getDOMNode(e.currentTarget.one('span')).nextSibling.data);
      });
   });
}

function InitSurburbList(){
  YUI().use('node',function(node){
    var input = node.one('#report-bar .extension-auto-complete input');
    var dom_input = node.Node.getDOMNode(input);
    dom_input.ext_onchange = function(searchStr){
      if(zoyoe.map){
         zoyoe.map.TargetPlace(searchStr,"AutoCompJSON");
      } else {
         zoyoe.ALERT("Map not loaded");
      }
    }
  });
}

function InitControlPanel(){
  YUI().use('dd-plugin', function(Y){
      var node = Y.one('#config-bar');
      node.plug(Y.Plugin.Drag);
      node.dd.addHandle('div.window-title');
  });
  for(var i=0;i<config.choice.length;i++){
    InitChoiceControl(config.choice[i]);
  }
  for(var i=0;i<config.combo.length;i++){
    InitComboControl(config.combo[i]);
  }
  InitSurburbList();
}

function GetMapArea(){
  return {left:0,top:0
  ,width:document.getElementById('map-info').offsetWidth
  ,height:document.getElementById('map-info').offsetHeight};
}

function RemoveFromArray(list,ele){
   var i = 0;
   for(;i<list.length;i++){
     if(list[i] == ele){
        break;
     }
   }
   if(i<list.length){
      list.splice(i,1);
   }
}
function RefreshServicesInRightDock(groups){
  YUI().use('node',function(node){
    var eles = new Array();
    var limit = 13;
    var main_tag = true;
    for(var i=0;i<groups.length;i++){
      if(groups[i].service_list.length != 0){
        var service = groups[i].service_list[0];
        if(service.active){
          eles.push(groups[i].service_list[0]);
          service.in_square = true;
        }
      }
    }
    node.all('#right-bar-dock div.cicon').each(function(n){
      var service = node.Node.getDOMNode(n).service;
      if(service){
        if(service.in_square){
          limit -= 1;
          main_tag = false;
          RemoveFromArray(eles,service);
        }else{
          node.Node.getDOMNode(n).service = null;
          zoyoe.async_queue.pause(); 
          zoyoe.fade_list.push(n);
          zoyoe.async_queue.run(); 
        }
      }
    });
    var gicon = node.one('#right-bar-dock div.lane div.icon');
    var gservice = node.Node.getDOMNode(gicon).service;
    if(gservice && gservice.in_square){
      limit -= 1;
      RemoveFromArray(eles,gservice);
      main_tag = false;
    }else{
      main_tag = true;
    }
    for(var i=0;limit > 0&&i<eles.length;i++){
      var service = eles[i];
      if(service.active){
        ShowServiceInRightDock(service,zoyoe.dock_style,main_tag);
        limit -= 1;
        main_tag = false;
      }
    }
  });
}

function SwitchPanel(h){
  YUI().use('node',function(node){
    if(h.shrink){
      h.innerHTML = "&#9666";
      var n = node.one('#config-bar');
      n.setStyle('width',"260px");
      n.setStyle('height',"");
      var m = node.one('#config-bar .window-title');
      m.setStyle('width','260px');
      var dummy = node.one('#config-bar .dummy');
      dummy.setStyle('display','none');
      n.setStyle('overflow',"show");
      h.shrink = false;
    }else{
      h.innerHTML = "&#9656";
      var n = node.one('#config-bar');
      n.setStyle('width',"100px");
      n.setStyle('height',"20px");
      var m = node.one('#config-bar .window-title');
      m.setStyle('width',"80px");
      var dummy = node.one('#config-bar .dummy');
      dummy.setStyle('display','block');
      h.shrink = true;
      n.setStyle('overflow',"hidden");
    }
  });
}

/*
 * Component
 */


function SwitchPlaceJSON(result){
  if(result.resourceSets){
    if(result.resourceSets[0].estimatedTotal = 0){
      zoyoe.ALERT('Address Not Found !!');
    }
    else if(result.resourceSets[0].estimatedTotal = 1){
      var resources = result.resourceSets[0].resources;
      if(resources.length == 0){
        BuildErrorMsg('Address Not Found !!');
      }else if(resources.length == 1){
        var c = resources[0].point.coordinates;
        zoyoe.map.map.setView({center:new Microsoft.Maps.Location(c[0],c[1])});
      }else{
        var select = "<form name='switch-place'><select name='sel'>";
        for(var i = 0; i < resources.length; i++){
          var option_val = resources[i].point.coordinates.join(",");
          select += "<option value='" + option_val + "'>"
            +resources[i].address.formattedAddress+"</option>";
        }
	      select += "</select></form>";
        zoyoe.ui.GeneralAlert(select,"Ambiguious Address, Please Make It Clear"
          ,function(){
          var select = document.forms['switch-place'].sel.value;
          var c = select.split(",");
          zoyoe.map.map.setView({center:new Microsoft.Maps.Location(c[0],c[1])});
        },false);
        zoyoe.ALERT("Ambiguious Address, Please Make It Clear !!");
      }
    }
    else{
      zoyoe.ALERT('Multi Address Found,Please Make It Clear !!');
    }
  }
}
