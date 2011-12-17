game.sign = function(n){
  if (n >0){return 1;}
  else if (n < 0){return -1;}
  else{return 0;}
}

zoyoe.game.instance = function(cells,path){
   var self = this;
   var parent = null;
   this.cells = cells;
   this.path = path;
   var ns = neighbours(this.cells);
   this.acquire = function(ps){
     for(var i=0;i<ps.length;i++){
       if (ps[i].x < 0 || this.cells.length <= ps[i].x
            || ps[i].y < 0 || this.cells[0].length <= ps[i].y
            || this.path[ps[i].x][ps[i].y] == 1){return false;}
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
   this.pixel2targets = function(top,left,vtop,vleft){
     var vt = game.sign(vtop); 
     var vl = game.sign(vleft); 
     return [{x:Math.floor((top+50+50*vt)/100),y:Math.floor((left+50+50*vl)/100)}]
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
          main.targets.push({bound:20,remain:20,vtop:0,vleft:-5,ele:e});
        }
        main.moveRight = function(e){
          main.targets.push({bound:20,remain:20,vtop:0,vleft:5,ele:e});
        }
        main.moveTop = function(e){
          main.targets.push({bound:20,remain:20,vtop:-5,vleft:0,ele:e});
        }
        main.moveBottom = function(e){
          main.targets.push({bound:20,remain:20,vtop:5,vleft:0,ele:e});
        }
        return main;
      }
    case 3: 
       var monster = new game.actor.monster(info[1],info[2]);
       this.actors[info[1]] = monster;
       return monster;
    case 4: 
       var monster_container = new game.obstcal.mstc(info[1],info[2]);
       this.actors[info[1]] = monster_container;
       return monster_container;
 
    }
  }
  this.plantBomb = function(idx){
    var self = this;
    var main = this.actors['main']; 
    if(main.targets.length > 0){
      return;
    }
    var p = main.position();
    var actcell = this.pixel2cell(p.top,p.left);
    var pos = this.cell2pixel(actcell.x,actcell.y);
    var bomb = this.bombs.pop();
    if(bomb){
      bomb.position(pos.top,pos.left);
      var frame = parent.getFrame(0);
      var track = parent.trackClip(frame,bomb);
      track.counting = 120; 
      $("#panel .bomb .number").html(this.bombs.length);
      this.path[actcell.x][actcell.y] = 1;
      track.action = function(){
        var fame = parent.getFrame(0);
        if(track.counting > 0 ){
          track.counting -= 1;
        }else if(track.counting == 0){
          track.counting -= 1;
          var tracks = frame.getClips();
          var srcidx = self.cells[0].length * actcell.x + actcell.y;
          for( t in tracks){
            var cell = self.pixel2cell(tracks[t].top,tracks[t].left);
            var cellidx = self.cells[0].length * cell.x + cell.y;
            if(ns(srcidx,cellidx)){
              if(tracks[t].bomb!=undefined){
                tracks[t].bomb();
              }
            }
          }
          frame.untrackClip(track);
          self.path[actcell.x][actcell.y] = 0;
        }else{
          return;
        } 
      }
    }
  }
  this.route_eles = [];
  this.bombs = [];
  this.onMouseClick = function(top,left){
    var cell = this.pixel2cell(top,left);
    var main = this.actors['main'];
    var p = parent.getFrame(0).getTrack(this.actors['main'].name()).clearTailTargets();
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
        this.clip.stop()
      }else{
        this.clip.play()
        if(this.clip.targets[0].remain >0){
          if(this.clip.targets[0].remain == this.clip.targets[0].bound){
            if(this.clip.targets[0].vtop>0){
              this.clip.towardsBottom();
            }else if(this.clip.targets[0].vtop<0){
              this.clip.towardsTop();
            }else if(this.clip.targets[0].vleft<0){
              this.clip.towardsLeft();
            }else if(this.clip.targets[0].vleft>0){
              this.clip.towardsRight();
            }
          }
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
    maintrack.clearTailTargets = function(){
      var main = this.clip;
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
      return {top:this.top+rt,left:this.left+rl};
    } 
    function initMonster(mtrack,v){
      mtrack.clip.targets = [{vtop:v.vt,vleft:v.vl}];
      mtrack.action = function(){
        var top = this.top + this.clip.targets[0].vtop;
        var left = this.left + this.clip.targets[0].vleft;
        var ps = self.pixel2targets(top,left,this.clip.targets[0].vtop,this.clip.targets[0].vleft);
        if(self.acquire(ps)){
          this.left += this.clip.targets[0].vleft;
          this.top += this.clip.targets[0].vtop;
        }else{
          this.clip.targets[0].vtop = 0 - this.clip.targets[0].vtop;
          this.clip.targets[0].vleft = 0 - this.clip.targets[0].vleft;
        }
      }
    }
    function initMContainer(name,mname,v){
      var mctrack = frame.getTrack(name); 
      var cell = self.pixel2cell(mctrack.top,mctrack.left);
      mctrack.clip.targets = [{vtop:v.vt,vleft:v.vl}];
      mctrack.bomb = function(){
        var m = new game.actor.monster(mname,v);
        self.actors['mname'] = m;
        parent.insertClip(m);
        var frame = parent.getFrame(0);
        m.position(this.top,this.left);
        var track = frame.trackClip(m);
        mctrack.action = function(){
          frame.untrackClip(mctrack);
          track.clip.targets = [{vtop:v.vt,vleft:v.vl}];
          track.action = function(){
            var left = this.left + this.clip.targets[0].vleft;
            var top = this.top + this.clip.targets[0].vtop;
            var ps = self.pixel2targets(top,left,this.clip.targets[0].vtop,this.clip.targets[0].vleft);
            if(self.acquire(ps)){
              this.left += this.clip.targets[0].vleft;
              this.top += this.clip.targets[0].vtop;
            }else{
              this.clip.targets[0].vleft = 0 - this.clip.targets[0].vleft;
              this.clip.targets[0].vtop = 0 - this.clip.targets[0].vtop;
            }
          }
          self.path[cell.x][cell.y] = 0;
          mctrack.action = function(){return;};
        }
      }
    }
    for (var n in this.actors){
      if (this.actors[n].type == game.actortype.GENERAL_MONSTER){
         var mtrack = frame.getTrack(this.actors[n].name()); 
         initMonster(mtrack,this.actors[n].para);
      }else if(this.actors[n].type == game.actortype.GENERAL_MONSTER_CONTAINER){
         initMContainer(this.actors[n].name(),zoyoe.game.newName(),this.actors[n].para);
      }
    }
    for(var i=0;i<3;i++){
      var b = new game.actor.bomb();
      this.bombs.push(b);
      parent.insertClip(b);
    }
  } 
}


