var drag_object = null;
var shadow_object = null;

function n2px(n){
  return n+'px';
}
function px2n(px){
  return parseInt(px);
}

function centerY(obj){
  return obj.offsetHeight/2+obj.offsetTop;
}

function GetTop(obj){
  var t = 0;
  var o = obj;
  do{
    t += o.offsetTop;
  }while(o = o.offsetParent);
  return t;
}

function GetLeft(obj){
  var t = 0;
  var o = obj;
  do{
    t += o.offsetLeft;
  }while(o = o.offsetParent);
  return t;
}

function MouseCoords(ev){ 
  var ev = ev || window.event;
  if(ev.pageX && ev.pageY){ 
      return {x:ev.pageX, y:ev.pageY}; 
  } 
  return { 
    x:ev.clientX + document.body.scrollLeft - document.body.clientLeft, 
    y:ev.clientY + document.body.scrollTop  - document.body.clientTop 
  }; 
} 

function MouseMove(ev){ 
   var mouse_pos = MouseCoords(ev); 
   if(drag_object != null){
      var offset_x = mouse_pos.x - drag_object.fix.x;
      var offset_y = mouse_pos.y - drag_object.fix.y;
      if(drag_object.drag(offset_x,offset_y)){
        drag_object.fix = mouse_pos;
      }else{
        drag_object.drop(offset_x,offset_y);
        drag_object = null;
        zoyoe.ui.ActivateContent();
      }
   }
}

function MouseUp(ev){
   var mouse_pos = MouseCoords(ev); 
   if(drag_object){
      var offset_x = mouse_pos.x - drag_object.fix.x;
      var offset_y = mouse_pos.y - drag_object.fix.y;
      drag_object.drop(offset_x,offset_y)
      zoyoe.ui.ActivateContent();
      drag_object = null;
   };
} 

function MarkAsDrag(obj,handler,mcb,dcb,scb){
  obj.drag = mcb;
  if(dcb){
    obj.drop= dcb;
  }
  handler.onmousedown = function(ev){
     zoyoe.ui.HibernateContent(true);
     if(ev){ev.preventDefault();}
     drag_object = obj;
     drag_object.fix = MouseCoords(ev);
     if(scb){scb();}
  }
}
function MarkAsArrangeV(p,obj,handler){
  var pa = p;
  var container = document.getElementById('dd-container');
  function drag(offset_x,offset_y){
    var next = null;
    var ceil = GetTop(shadow_object) - shadow_object.offsetHeight/2;
    var bot = GetTop(shadow_object) + shadow_object.offsetHeight/2;
    container.style.top = n2px(px2n(container.style.top)+offset_y);
    container.style.left = n2px(px2n(container.style.left)+offset_x);
    if (container.offsetTop>ceil && container.offsetTop<bot){return true;}
    for(var i=0;i<p.childNodes.length;i++){
      if(centerY(p.childNodes[i])>=centerY(container)){
        next = p.childNodes[i];
        break;
      }
    }
    if(next!=shadow_object){ 
      if(next){
        p.removeChild(shadow_object);
        p.insertBefore(shadow_object,next);
      }else{
        if(shadow_object.nextSibling){
          p.removeChild(shadow_object);
          p.appendChild(shadow_object);
        }
      }
    }
    return true;
  }
  function drop(offset_x,offset_y){
    var next = null;
    for(var i=0;i<p.childNodes.length;i++){
      if(centerY(p.childNodes[i])>=obj.fix.y+obj.offsetHeight/2+offset_y){
       next = p.childNodes[i];
       break;
      }
    }
    container.style.display = "none"
    container.removeChild(obj);
    p.replaceChild(obj,shadow_object);
  }
  function startDrag(){
    container.className = pa.className;
    container.style.display = "block";
    shadow_object.style.position = "relative";
    shadow_object.style.width = n2px(obj.offsetWidth-2);
    shadow_object.style.height = n2px(obj.offsetHeight-2);
    shadow_object.style.display = "block";
    p.replaceChild(shadow_object,obj);
    container.insertBefore(obj,container.firstChild);
    container.style.top = n2px(GetTop(shadow_object));
    container.style.left = n2px(GetLeft(shadow_object));
    obj.style.display = "block";
  }
  MarkAsDrag(obj,handler,drag,drop,startDrag);
}
function MarkAsScrollH(obj){
  var conv = obj;
  /* Following is the drag element we are going to use */
  var drag = obj.getElementsByTagName('div')[0];
  /* Following is the Container Node */
  var p = obj.parentNode;
  /* Following is the Content Node */
  var cxt = obj.parentNode.getElementsByTagName('div')[0];
  drag.style.top = "0px";
  obj.Reset = function(){
    cxt.style.top = "0px";
    drag.style.top = "0px";
  }
  function drag_handler(offset_x,offset_y){
    if(offset_y > conv.offsetHeight - drag.offsetTop - drag.offsetHeight){
       offset_y = conv.offsetHeight - drag.offsetTop - drag.offsetHeight;
       return false;
    }
    else if(offset_y + drag.offsetTop < 0){
       return false;
    }else{
      var nt = offset_y+px2n(drag.style.top);
      drag.style.top = n2px(nt);
      var per = nt/(conv.offsetHeight-10);
      cxt.style.top = n2px(per*(p.offsetHeight-cxt.offsetHeight));
      return true;
    }
  }
  drag.drop = function(offset_x,offset_y){
    //alert(offset_x+','+offset_y)
  };
  MarkAsDrag(drag,drag,drag_handler);
}
function MarkAsScroll(obj,cb,dcb){
  var conventionlist = obj.getElementsByTagName('div');
  var blank = conventionlist[0];
  var draglow = conventionlist[1];
  var fill = conventionlist[2];
  var draghigh = conventionlist[3];
  function dragl (offset_x,offset_y){
    if (offset_x >obj.offsetWidth - blank.offsetWidth -22){
      offset_x = obj.offsetWidth - blank.offsetWidth-22;
      return false;
    }
    if(blank.offsetWidth+offset_x<=0){
      blank.style.width = n2px(0);
      fill.style.width = n2px(fill.offsetWidth+blank.offsetWidth);
      return false;
    }else{
      blank.style.width = n2px(blank.offsetWidth+offset_x);
      if(fill.offsetWidth-offset_x<=0){
        fill.style.width = n2px(0);
      }else{
        fill.style.width = n2px(fill.offsetWidth-offset_x);
      }
      return true;
    }
  }
  draglow.drop = function(offset_x,offset_y){
    dcb((blank.offsetWidth*100)/obj.offsetWidth,(blank.offsetWidth*100+fill.offsetWidth*100)/obj.offsetWidth);
  }
  function dragh(offset_x,offset_y){
    if(offset_x>obj.offsetWidth-draghigh.offsetLeft-13){
       offset_x = obj.offsetWidth-draghigh.offsetLeft-13;
       return false;
    }
    if(offset_x + fill.offsetWidth <= 0){
      fill.style.width = n2px(0);
      return false;
    }else{
      fill.style.width = n2px(fill.offsetWidth+offset_x);
      return true;
    }
  }
  draghigh.drop = function(offset_x,offset_y){
    dcb((blank.offsetWidth*100)/obj.offsetWidth,(blank.offsetWidth*100+fill.offsetWidth*100)/obj.offsetWidth);
  }
  MarkAsDrag(draglow,draglow,
  function (offset_x,offset_y){
    var r = dragl(offset_x,offset_y);
    cb((blank.offsetWidth*100)/obj.offsetWidth,(blank.offsetWidth*100+fill.offsetWidth*100)/obj.offsetWidth);
    return r;
  });
  MarkAsDrag(draghigh,draghigh,
  function (offset_x,offset_y){
    var r = dragh(offset_x,offset_y);
    cb((blank.offsetWidth*100)/obj.offsetWidth,(blank.offsetWidth*100+fill.offsetWidth*100)/obj.offsetWidth);
    return r;
  });
}
function InitDrag(s_object){
  document.onmousemove = MouseMove; 
  document.onmouseup = MouseUp; 
  shadow_object = s_object;
}

function Clip(step,stop){
   this.frame = 0;
   this.Step = function(){
    step(this.frame);
    this.frame ++;
   }
   this.Stop = function(){
    stop();
   }
}

function TimeLine(){
  var cliplist = new Array();
  var time_event = null;
  var self = this;
  var NewClip = function(clip){
    cliplist.push(clip);
  }
  var TerminateClip = function(clip){
  }
  var Step = function(){
    for(var i=0;i<cliplist.length;i++){
      cliplist[i].Step();
    }
    alert('step');
  }
  var Stop = new function(){
    for(var i=0;i<cliplist.length;i++){
      cliplist[i].Stop();
    }
  }
}

function BuildDropList(ul_ele,cur_ele,name_array){
}
function BuildDistance(ll1,ll2){
  var lat1 = ll1.lat;
  var lat2 = ll2.lat;
  var lon1 = ll1.long;
  var lon2 = ll2.long;
  var R = 6371;
  var dLat = (lat2-lat1).toRad();
  var dLon = (lon2-lon1).toRad(); 
  var a = Math.sin(dLat/2) * Math.sin(dLat/2) +
        Math.cos(lat1.toRad()) * Math.cos(lat2.toRad()) * 
        Math.sin(dLon/2) * Math.sin(dLon/2); 
  var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
  var d = R * c;
  return d;
}
