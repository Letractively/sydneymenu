function document_load(){
  YUI().use('node','io-form',function(Y){
    if(zoyoe.ElementExtension){
      zoyoe.ElementExtension.BuildExtensionElements();
    }
    zoyoe.InitZoyoe(false,Y);
    zoyoe.admin = InitAdmin(zoyoe);
    new MapInfoCore(function(rmap){
      sdist(rmap)
    },null,"map-info")
  });
}

function sdist(ret_map){
  YUI().use('io-form','node',function(Y){
    var uri = ("/core/data/getservices/?tstmp={{TIME_STAMP}}");
    zoyoe.map = ret_map;
    function complete(io,o,args){
      var s_element = o.responseXML.documentElement.getElementsByTagName('SERVICE');
      for(var i=0;i<s_element.length;i++){
        var element = s_element[i];
        var service = new Service(element);
        ret_map.AddService(service);
      }
      var s_element = o.responseXML.documentElement.getElementsByTagName('REPORT');
      foreach(s_element,function(element){
        var report = new ServiceReport(element);
        ret_map.AddService(report);
      });
 
      ret_map.ShiftZoom(true);
      InitDrag();
      var scroll_h = Y.one('#right-bar-dock .div-scroll div.hscroll');
      var scroll_h_ele = Y.Node.getDOMNode(scroll_h);
      MarkAsScrollH(scroll_h_ele);
      var float_sh = Y.one('#float-info .div-scroll div.hscroll');
      var float_sh_ele = Y.Node.getDOMNode(float_sh);
      MarkAsScrollH(float_sh_ele);
      InitControlPanel();
      window.onresize = function(){
        //ret_map.map.Resize();
      }
    }
    Y.on('io:complete',complete);
    var request = Y.io(uri);
  });
  return true;
}

YUI().use('async-queue','stylesheet',function(Y){
  zoyoe.async_queue = new Y.AsyncQueue(); 
  zoyoe.fade_list = new Array();
  zoyoe.stop_queue = function(){return false;}
  zoyoe.async_queue.add({
    fn:function(){
      if(zoyoe.fade_list.length ==0){
        zoyoe.async_queue.pause();
      }else{
        for(var i=0;i<zoyoe.fade_list.length;i++){
          var opacity = zoyoe.fade_list[i].getStyle('opacity') - 0.1; 
          zoyoe.fade_list[i].setStyle('opacity',opacity);
          if(opacity < 0.1){
            var n = zoyoe.fade_list[i];
            zoyoe.fade_list.splice(i,1);
            n.remove();
          }
        }
      }
    },timeout:50,until:zoyoe.stop_queue});
  zoyoe.async_queue.run();
});

function ResetShortCut(i){
  YUI().use('node',function(yui_node){
    var icon_containers = yui_node.all('#panel .gicon');
    var innerHTML = icon_containers.item(i).get('innerHTML');
    icon_containers.item(i).set('innerHTML','');
    icon_containers.item(i).set('innerHTML',innerHTML);
  });
}

function ShowServiceInRightDock(service,style,main_tag){
  if(zoyoe.has_right_dock == false){return;/* Ugly Code make sure we have right dock */}
  YUI().use('node',function(node){
    var n = node.one('#right-bar-dock div.icons');
    var sdiv = null;
    if(style == 'COMPACT' || !main_tag){
      sdiv = node.Node.create(
        "<div class='cicon' onclick=\"window.location.href='/core/service/"+service.name+"'\">"
        +"<img src='/core/data/res/"+service.name+'/'+service.icon+"/?sc=true&cache=1' ></img>"
        +"</div>"
        );
      n.append(sdiv); 
   }else{
      sdiv = node.one('#right-bar-dock div.lane div.icon');
      node.Node.getDOMNode(sdiv).service = service;
      sdiv.on('click',function(){
        window.location.href='/core/service/'+service.name;
      });
      sdiv.set('innerHTML',
        "<img src='/core/data/res/"+service.name+'/'+service.icon+"/?sc=true&cache=1'></img>"
        +"<div class='info'><a>"
        +service.name+"</a><p>"+service.address+"</p></div>"
        +"</div>");
    }
    sdiv.on('mouseover',function(){
     var gp = zoyoe.map.map.tryLocationToPixel(service.loc,Microsoft.Maps.PixelReference.page);
      //alert(gp);
      document.getElementById('raw-left').style.width = n2px(gp.x - 13);
      document.getElementById('raw-right').style.left = n2px(gp.x + 13);
      document.getElementById('raw-top').style.height = n2px(gp.y - 13);
      document.getElementById('raw-bottom').style.top = n2px(gp.y + 13);
      document.getElementById('raw-left').style.display = "block";
      document.getElementById('raw-right').style.display = "block";
      document.getElementById('raw-top').style.display = "block";
      document.getElementById('raw-bottom').style.display = "block";
    });
    sdiv.on('mouseout',function(){
      var gp = zoyoe.map.map.tryLocationToPixel(service.loc,Microsoft.Maps.PixelReference.page);
      document.getElementById('raw-left').style.display = "none";
      document.getElementById('raw-right').style.display = "none";
      document.getElementById('raw-top').style.display = "none";
        document.getElementById('raw-bottom').style.display = "none";
      });
    node.Node.getDOMNode(sdiv).service = service;
  });
}
