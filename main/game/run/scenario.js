var scenario1 = (function createInstance(){
   var cm1 = [3,"m1",{vt:2,vl:0}];
   var cm2 = [4,"mc2",{vt:0,vl:2}];
   var cm3 = [4,"mc3",{vt:0,vl:2}];
   var cmain = [2,"main"];
   var cells = 
   [
    [1,1,  0  ,0,1,0,    0,0,1],
    [0,0,  0  ,1,0,cm2,  0,0,1],
    [1,0,  1  ,0,0,1,    1,1,0],
    [0,cm1,cm3,0,1,cmain,0,0,0],
    [0,0,  1,  0,0,0,    0,1,1],
    [1,1,  0,  0,0,0,    0,0,1],
   ]
   var path = 
   [
    [1,1,0,0,1,0,0,0,1],
    [0,0,0,1,0,1,0,0,1],
    [1,0,1,0,0,1,1,1,0],
    [0,0,1,0,1,0,0,0,0],
    [0,0,1,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,1],
   ];
   return (new zoyoe.game.instance(cells,path));
})();

var scenario2 = (function createInstance(){
   var cm1 = [3,"m1",{vt:2,vl:0}];
   var cm2 = [4,"mc2",{vt:0,vl:2}];
   var cm3 = [4,"mc3",{vt:0,vl:2}];
   var cmain = [2,"main"];
   var cells = 
   [
    [1,1,  0  ,0,1,0,    0,0,1],
    [0,0,  0  ,1,0,cm2,  0,0,1],
    [1,0,  1  ,0,0,1,    1,1,0],
    [0,cm1,cm3,0,1,cmain,0,0,0],
    [0,0,  1,  0,0,0,    0,1,1],
    [1,1,  0,  0,0,0,    0,0,1],
   ]
   var path = 
   [
    [1,1,0,0,1,0,0,0,1],
    [0,0,0,1,0,1,0,0,1],
    [1,0,1,0,0,1,1,1,0],
    [0,0,1,0,1,0,0,0,0],
    [0,0,1,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,1],
   ];
   return (new zoyoe.game.instance(cells,path));
})();

var scenarios = {basic:[scenario1,scenario1]}

function getScenario(set,idx){
  return scenarios[set][idx]
}

$.fn.extend({ 
        disableSelection : function() { 
                this.each(function() { 
                        this.onselectstart = function() { return false; }; 
                        this.unselectable = "on"; 
                        $(this).css('-moz-user-select', 'none'); 
                        $(this).css('-webkit-user-select', 'none'); 
                }); 
        } 
});

function buildInfo(inst){
  $("#panel .bomb .number").html(inst.bombs.length);
}
function bindClickHandler(element,handler){
  if(window.Touch){
    element.addEventListener("touchstart",handler,false)
  }else{
    element.addEventListener("click",handler,false)
  }
}

function getUrlVars()
{
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++)
    {
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
    }
    return vars;
}

function loadScenario(){
    var singleton = {};
    var sc = getUrlVars();
    singleton.inst = getScenario(sc.set,sc.idx);
    var jq_root = $('#root');
	var env = new zoyoe.game.env($('#root').get(0),30,40,0);
    bindClickHandler($("#root").get(0),function(e){
        var touch = e;
        if(e.type == "touchstart"){
          touch = e.touches[0];
        }
        e.stopPropagation();
        e.cancelBubble = true;
        e.preventDefault();
        var p = jq_root.offset();
        singleton.inst.onMouseClick(touch.pageY - p.top,touch.pageX - p.top);
    });
    $("body").get(0).ontouchmove = function(e){
      e.preventDefault();
    }
    $("#panel .bombtouch").click(function(e){
      singleton.inst.plantBomb();
    });
    $("#panel .replay").click(function(e){
      env.reset();
      singleton.inst = getScenario(sc.set,sc.idx);
      var root = env.root();
      var clip = new zoyoe.game.clip('move',$("<div></div>").get(0));
      var map = new game.map(singleton.inst ,clip);
      map.generate();
      root.insertClip(clip);
      root.trackClip(root.getFrame(0),clip);
      buildInfo(singleton.inst);
      env.run();
    });
    var root = env.root();
    var clip = new zoyoe.game.clip('move',$("<div></div>").get(0));
    var map = new game.map(singleton.inst ,clip);
    map.generate();
    root.insertClip(clip);
    root.trackClip(root.getFrame(0),clip);
    buildInfo(singleton.inst);
    env.run();
}

function dialog(message,actionlist){
  var dialog = $("dialog");
  if(!dialog){
    dialog = $("<div id = 'dialog'></div>");
    dialog.css({"top":n2px(-100000000)
      ,"left":n2px(-10000000)
      ,"position":"fixed"
      });
  }
}
