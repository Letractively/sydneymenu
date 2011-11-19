var game = {}
game.VOID = 0;
game.PATH = 1;
game.OBSTCAL = 2;
game.ITEM = 2;
game.BLOCK_SZ = 100;
game.path = {}
game.obstcal = {}
game.actor = {}
game.path.NORMAL_IMG = "res/path/normal.png";
game.path.NORMAL_CENTER = {top:0,left:0};
game.obstcal.BOWL_IMG = "res/obstcal/bowl.png";
game.obstcal.MSTC_IMG = "res/obstcal/monster_container.png";
game.actor.MAIN_IMG = "res/actor/mainactor.png";
game.actor.MONSTER_IMG = "res/actor/monster1.png";
game.actor.BOMB_IMG = "res/actor/bomb.png";

game.path.normal = function(){
  return null;
}
game.obstcal.mstc = function(name){
  var ele = $("<div class='block-normal'><img src='"+game.obstcal.MSTC_IMG+"'></image></div>").get(0);
  ele.style.width = n2px(game.BLOCK_SZ);
  ele.style.height = n2px(game.BLOCK_SZ);
  var clip = (new zoyoe.clip(name,ele));
  return clip;
}
game.obstcal.bowl = function(){
  var ele = $("<div class='block-normal'><img src='"+game.obstcal.BOWL_IMG+"'></image></div>").get(0);
  ele.style.width = n2px(game.BLOCK_SZ);
  ele.style.height = n2px(game.BLOCK_SZ);
  var img = ele.getElementsByTagName("img")[0];
  img.style.position = "relative";
  img.style.left = "-20px";
  var clip = (new zoyoe.clip(zoyoe.newName(),ele));
  return clip;
}
game.actor.bomb = function(){
  var ele = $("<div class='block-normal'><img src='"+game.actor.BOMB_IMG+"'></image></div>").get(0);
  ele.style.width = n2px(game.BLOCK_SZ);
  ele.style.height = n2px(game.BLOCK_SZ);
  var img = ele.getElementsByTagName("img")[0];
  img.style.position = "relative";
  img.style.top = "48px";
  img.style.left = "35px";
  var clip = (new zoyoe.clip(zoyoe.newName(),ele));
  return clip;
}
game.actor.main = function(name){
  var ele = $("<div class='block-normal'><img src='"+game.actor.MAIN_IMG+"'></image></div>").get(0);
  ele.style.width = n2px(game.BLOCK_SZ);
  ele.style.height = n2px(game.BLOCK_SZ);
  var img = ele.getElementsByTagName("img")[0];
  img.style.position = "relative";
  img.style.left = "8px";
  var clip = (new zoyoe.clip(name,ele));
  return clip;
}
game.actor.monster = function(name){
  var ele = $("<div class='block-normal'><img src='"+game.actor.MONSTER_IMG+"'></image></div>").get(0);
  ele.style.overflow = "hidden";
  ele.style.width = n2px(game.BLOCK_SZ);
  ele.style.height = n2px(game.BLOCK_SZ);
  var img = ele.getElementsByTagName("img")[0];
  img.style.position = "relative";
  img.style.left = "8px";
  var clip = (new zoyoe.clip(name,ele));
  return clip;
}

game.map = function(inst,clip){
  this.generate = function(){
    var cells = this.instance.cells;
    for(var r=0;r<cells.length;r++){
      for (var l=0;l<cells[r].length;l++){
        var cell = inst.itemInit(cells[r][l]);
        if(cell){
          clip.insertClip(cell);
          var pos = this.instance.cell2pixel(r,l);
          var p = cell.position(pos.top,pos.left);
          var frame = clip.getFrame(0);
          var cliptrack = clip.trackClip(frame,cell);
        }
      }
    }
    inst.initStage(this.clip);
  };
  this.instance = inst;
  this.clip = clip;
}
function Instance(){
   var self = this;
   var parent = null;
   var cm1 = [3,"m1"];
   var cm2 = [4,"mc1"];
   var cm3 = [4,"mc2"];
   var cmain = [2,"main"];
   this.cells = 
   [
    [1,1,  0  ,0,1,0,    0,0,1],
    [0,0,  0  ,1,0,cm2,  0,0,1],
    [1,0,  1  ,0,0,1,    1,1,0],
    [0,cm1,cm3,0,1,cmain,0,0,0],
    [0,0,  1,  0,0,0,    0,1,1],
    [1,1,  0,  0,0,0,    0,0,1],
    [0,1,  0,  1,0,1,    1,1,0],
   ]
   this.path = 
   [
    [1,1,0,0,1,0,0,0,1],
    [0,0,0,1,0,1,0,0,1],
    [1,0,1,0,0,1,1,1,0],
    [0,0,1,0,1,0,0,0,0],
    [0,0,1,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,1],
    [0,1,0,1,0,1,1,1,0],
   ]
   this.acquire = function(ps){
     for(var i=0;i<ps.length;i++){
       if (ps[i].x < 0 || this.cells.length <= ps[i].x
            || ps[i].y < 0 || this.cells[0].length <= ps[i].y
            || this.cells[ps[i].x][ps[i].y] == 1){return false;}
     }
     return true;
   }; 
 
   this.cell2pixel = function(x,y){
     return {top:x*100,left:y*100};
   };
   this.pixel2cell = function(top,left){
     return {x:Math.floor(top/100),y:Math.floor(left/100)}
   };
   this.pixel2cells = function(top,left){
     return [{x:Math.floor(top/100),y:Math.floor(left/100)},
             {x:Math.floor(top/100),y:Math.floor((left + 99)/100)},
             {x:Math.floor((top + 99)/100),y:Math.floor(left/100)},
             {x:Math.floor((top+99)/100),y:Math.floor((left+99)/100)}]
   };
   this.pathExtractor = function(x,y){
     var cells = this.path;
     var es = edges(cells);
     var idx = this.cells[0].length * x + y;
     var path = shortestPath(es,cells[0].length * cells.length,idx);
     return function(x,y){
       var idx = cells[0].length * x + y;
       return constructPath(path,idx);
     }
   }
   this.actors = {};
   this.itemInit = function(info){
    var idx = info
    if(isNaN(info)){
      idx = info[0];
    }
    switch(idx){
    case 0: return null;
    case 1: return (new game.obstcal.bowl());
    case 2: {
        var main = new game.actor.main(info[1]);
        this.actors['main'] = main;
        main.is_actor = true;
        main.speed_top = 0;
        main.speed_left = 0;
        main.targets = [];
        main.moveLeft = function(e){
          main.targets.push({remain:20,vtop:0,vleft:-5,ele:e});
        }
        main.moveRight = function(e){
          main.targets.push({remain:20,vtop:0,vleft:5,ele:e});
        }
        main.moveTop = function(e){
          main.targets.push({remain:20,vtop:-5,vleft:0,ele:e});
        }
        main.moveBottom = function(e){
          main.targets.push({remain:20,vtop:5,vleft:0,ele:e});
        }
        main.clearTailTargets = function(){
          while(main.targets.length > 1){
            var target = main.targets.pop();
            target.ele.remove();
          }
          var rt = 0;
          var rl = 0;
          if(main.targets.length > 0){
            rt = main.targets[0].vtop*main.targets[0].remain;
            rl = main.targets[0].vleft*main.targets[0].remain;
          }
          return {top:main.top()+rt,left:main.left()+rl};
        }
        return main;
      }
    case 3: 
       var monster = new game.actor.monster(info[1]);
       this.actors[info[1]] = monster;
       return monster;
    case 4: 
       var monster_container = new game.obstcal.mstc(info[1]);
       this.actors[info[1]] = monster_container;
       return monster_container;
 
    }
  }
  this.plantBomb = function(idx){
    var main = this.actors['main']; 
    var p = main.position();
    var actcell = this.pixel2cell(p.top,p.left);
    var pos = this.cell2pixel(actcell.x,actcell.y);
    var bomb = this.bombs.pop();
    if(bomb){
      bomb.position(pos.top,pos.left);
      var frame = parent.getFrame(0);
      parent.trackClip(frame,bomb);
      $("#panel .bomb .number").html(this.bombs.length);
      this.path[actcell.x][actcell.y] = 1;
    }
  }
  this.route_eles = [];
  this.bombs = [];
  this.onMouseClick = function(top,left){
    var cell = this.pixel2cell(top,left);
    var main = this.actors['main'];
    var p = main.clearTailTargets();
    var actcell = this.pixel2cell(p.top,p.left); 
    var path = self.pathExtractor(actcell.x,actcell.y)(cell.x,cell.y);
    var st = '';
    var acy = actcell.y
    var acx = actcell.x
    for(var i=0;i<path.length;i++){
      var r = Math.floor(path[i]/this.cells[0].length);
      var l = path[i] % this.cells[0].length;
      var block = $("<div class='route'><div></div></div>");
      block.css({"top":n2px(r*100),"left":n2px(l*100)});
      $("#root").append(block);
      var x = Math.floor(path[i]/this.cells[0].length);
      var y = path[i] % this.cells[0].length;
      var v = acy - y;
      var h = acx - x;
      if(v < 0){
        main.moveRight(block);
      }else if (0 < v){
        main.moveLeft(block);
      }else if (h < 0){
        main.moveBottom(block);
      }else if (0 < h){
        main.moveTop(block);
      }
      acy = y;
      acx = x;
    }
  }
  this.initStage = function(p){
    parent = p;
    var frame = parent.getFrame(0);
    var self = this;
    var maintrack = frame.getTrack(this.actors['main'].name()); 
    maintrack.action = function(){
      if(this.clip.targets.length == 0){
         /* Nothing to Do */
      }else{
        if(this.clip.targets[0].remain >0){
          var rt = this.clip.targets[0].vtop * this.clip.targets[0].remain;
          var rl = this.clip.targets[0].vleft * this.clip.targets[0].remain;
          var ps = self.pixel2cells(this.top+rt,this.left+rl);
          if(self.acquire(ps)){
            this.top += this.clip.targets[0].vtop;
            this.left += this.clip.targets[0].vleft;
            this.clip.targets[0].remain -= 1;
          }else{
            this.clip.targets[0].ele.remove();
            this.clip.targets.shift();
          }
        }else{
          this.clip.targets[0].ele.remove();
          this.clip.targets.shift();
        }
      }
    }
    var m1track = frame.getTrack(this.actors['m1'].name()); 
    m1track.clip.targets = [{vtop:2,vleft:0}];
    m1track.action = function(){
      var top = this.top + this.clip.targets[0].vtop;
      var left = this.left;
      var ps = self.pixel2cells(top,left);
      if(self.acquire(ps)){
        this.top += this.clip.targets[0].vtop;
      }else{
        this.clip.targets[0].vtop = 0 - this.clip.targets[0].vtop;
      }
    }
/*
    var m2track = frame.getTrack(this.actors['m2'].name()); 
    m2track.clip.targets = [{vtop:0,vleft:2}];
    m2track.action = function(){
      var left = this.left + this.clip.targets[0].vleft;
      var top = this.top;
      var ps = self.pixel2cells(top,left);
      if(self.acquire(ps)){
        this.left += this.clip.targets[0].vleft;
      }else{
        this.clip.targets[0].vleft = 0 - this.clip.targets[0].vleft;
      }
    }
*/
    for(var i=0;i<3;i++){
      var b = new game.actor.bomb();
      this.bombs.push(b);
      parent.insertClip(b);
    }
  } 
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
function test(){
    var singleton = {};
    singleton.inst = new Instance();
    var jq_root = $('#root');
	var env = new zoyoe.env($('#root').get(0),30,10,0);
    $("#root").click(function(e){
        e.stopPropagation();
        e.cancelBubble = true;
        e.preventDefault();
        var p = jq_root.offset();
        singleton.inst.onMouseClick(e.pageY - p.top,e.pageX - p.top);
    });
    $("body").get(0).ontouchmove = function(e){
      e.preventDefault();
    }
    $("#panel .bomb").click(function(e){
      singleton.inst.plantBomb();
    });
    $("#panel .replay").click(function(e){
      env.reset();
      var inst = new Instance();
      singleton.inst = inst;
      var root = env.root();
      var clip = new zoyoe.clip('move',$("<div></div>").get(0));
      var map = new game.map(inst ,clip);
      map.generate();
      root.insertClip(clip);
      root.trackClip(root.getFrame(0),clip);
      buildInfo(singleton.inst);
      env.run();
    });
    var root = env.root();
    var clip = new zoyoe.clip('move',$("<div></div>").get(0));
    var map = new game.map(singleton.inst ,clip);
    map.generate();
    root.insertClip(clip);
    root.trackClip(root.getFrame(0),clip);
    buildInfo(singleton.inst);
    env.run();
}
