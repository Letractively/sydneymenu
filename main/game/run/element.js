var game = {}
game.VOID = 0;
game.PATH = 1;
game.OBSTCAL = 2;
game.ITEM = 2;
game.BLOCK_SZ = 100;
game.ACTOR_HEIGHT = 120;
game.path = {};
game.obstcal = {};
game.actor = {};
game.actortype = {};
game.path.NORMAL_IMG = "res/path/normal.png";
game.path.NORMAL_CENTER = {top:0,left:0};
game.obstcal.TREE_IMG = "res/obstcals/tree.png";
game.obstcal.TREECUT_IMG = "res/obstcals/treecut.png";
game.actor.MAIN_IMG = "res/actors/main.png";
game.actor.MONSTER_IMG = "res/actors/mob1.png";
game.actor.BOMB_IMG = "res/actors/bomb.png";
game.actortype.GENERAL_MONSTER = 1;
game.actortype.GENERAL_MONSTER_CONTAINER = 2;

game.path.normal = function(dec){
  var decoration = Math.floor(Math.random()*21); 
  if(decoration <= 2) {
    var ele = $("<div class='block-normal'><img src='res/ground/flower1.png'></image></div>").get(0);
    ele.style.width = n2px(game.BLOCK_SZ);
    ele.style.height = n2px(game.BLOCK_SZ);
    var clip = (new zoyoe.game.clip(name,ele));
    clip.zidxLock(0);
    return clip;
  }else if(decoration <= 4){
    var ele = $("<div class='block-normal'><img src='res/ground/flower2.png'></image></div>").get(0);
    ele.style.width = n2px(game.BLOCK_SZ);
    ele.style.height = n2px(game.BLOCK_SZ);
    var clip = (new zoyoe.game.clip(name,ele));
    clip.zidxLock(0);
    return clip;
  }else if(decoration == 5){
    var ele = $("<div class='block-normal'><img src='res/ground/stone.png'></image></div>").get(0);
    ele.style.width = n2px(game.BLOCK_SZ);
    ele.style.height = n2px(game.BLOCK_SZ);
    var clip = (new zoyoe.game.clip(name,ele));
    clip.zidxLock(0);
    return clip;
  }else{
    return null;
  }
}
game.obstcal.mstc = function(name,para){
  var ele = $("<div class='block-normal'><img src='"+game.obstcal.TREECUT_IMG+"'></image></div>").get(0);
  ele.style.width = n2px(game.BLOCK_SZ);
  ele.style.height = n2px(game.BLOCK_SZ);
  var clip = (new zoyoe.game.clip(name,ele));
  clip.para = para;
  clip.type = game.actortype.GENERAL_MONSTER_CONTAINER;
  return clip;
}
game.obstcal.tree = function(){
  var ele = $("<div class='block-normal'><img src='"+game.obstcal.TREE_IMG+"'></image></div>").get(0);
  ele.style.width = n2px(game.BLOCK_SZ);
  ele.style.height = n2px(game.BLOCK_SZ);
  var img = ele.getElementsByTagName("img")[0];
  img.style.position = "relative";
  img.style.top = "-50px";
  var clip = (new zoyoe.game.clip(zoyoe.game.newName(),ele));
  return clip;
}
game.actor.bomb = function(){
  var ele = $("<div class='block-normal'><img src='"+game.actor.BOMB_IMG+"'></image></div>").get(0);
  ele.style.width = n2px(game.BLOCK_SZ);
  ele.style.height = n2px(game.BLOCK_SZ);
  var img = ele.getElementsByTagName("img")[0];
  img.style.position = "relative";
  img.style.width = "100px";
  img.style.height = "100px";
  var clip = (new zoyoe.game.clip(zoyoe.game.newName(),ele));
  clip.stop();
  return clip;
}
game.actor.BuildMoveAction = function(clip){
  var ele = clip.element();
  var img = ele.getElementsByTagName("img")[0];
  clip.center(17,0);
  clip.appendFrames(160);
  var mainframe = clip.getFrame(0); 
  var moveTop = [clip.getFrame(1),clip.getFrame(6),
    clip.getFrame(11),clip.getFrame(16),clip.getFrame(20)];
  var moveBottom = [clip.getFrame(21),clip.getFrame(26),
    clip.getFrame(31),clip.getFrame(36),clip.getFrame(40)];
  var moveRight = [clip.getFrame(41),clip.getFrame(46),
    clip.getFrame(51),clip.getFrame(56),clip.getFrame(60)];
  var moveLeft = [clip.getFrame(61),clip.getFrame(66),
    clip.getFrame(71),clip.getFrame(76),clip.getFrame(80)];
 
  var top = 2040 - 120;
  for(var i=0;i<4;i++){
    moveLeft[i].setKeyframe(true);
    moveLeft[i].tmp = top;
    moveLeft[i].action = function(){
      img.style.top = "-"+this.tmp+"px";
    }
    top -= 120;
  }
  moveLeft[4].action = function(){
    clip.gotoAndPlay(61);
  }
  for(var i=0;i<4;i++){
    moveRight[i].setKeyframe(true);
    moveRight[i].tmp = top;
    moveRight[i].action = function(){
      img.style.top = "-"+this.tmp+"px";
    }
    top -= 120;
  }
  moveRight[4].action = function(){
    clip.gotoAndPlay(41);
  }
  for(var i=0;i<4;i++){
    moveBottom[i].setKeyframe(true);
    moveBottom[i].tmp = top;
    moveBottom[i].action = function(){
      img.style.top = "-"+this.tmp+"px";
    }
    top -= 120;
  }
  moveBottom[4].action = function(){
    clip.gotoAndPlay(21);
  }
  for(var i=0;i<4;i++){
    moveTop[i].setKeyframe(true);
    moveTop[i].tmp = top;
    moveTop[i].action = function(){
      img.style.top = "-"+this.tmp+"px";
    }
    top -= 120;
  }
  moveTop[4].action = function(){
    clip.gotoAndPlay(1);
  }
  clip.towardsTop = function(){
    clip.gotoAndPlay(1);
  }
  clip.towardsRight = function(){
    clip.gotoAndPlay(41);
  }
  clip.towardsLeft = function(){
    clip.gotoAndPlay(61);
  }
  clip.towardsBottom = function(){
    clip.gotoAndPlay(21);
  }
  clip.stand = function(){
    clip.gotoAndStop(0);
  }
  clip.stop();
}
game.actor.main = function(name){
  var ele = $("<div class='block-actor'><img src='"+game.actor.MAIN_IMG+"'></image></div>").get(0);
  ele.style.width = n2px(game.BLOCK_SZ);
  ele.style.height = n2px(game.ACTOR_HEIGHT);
  var img = ele.getElementsByTagName("img")[0];
  img.style.position = "relative";
  img.style.width = "100px";
  img.style.left = "0px";
  img.style.top = "0px";
  var clip = (new zoyoe.game.clip(name,ele));
  game.actor.BuildMoveAction(clip);
  return clip;
}
game.actor.monster = function(name,para){
  var ele = $("<div class='block-actor'><img src='"+game.actor.MONSTER_IMG+"'></image></div>").get(0);
  ele.style.width = n2px(game.BLOCK_SZ);
  ele.style.height = n2px(game.ACTOR_HEIGHT);
  var img = ele.getElementsByTagName("img")[0];
  img.style.position = "relative";
  img.style.width = "100px";
  img.style.left = "0px";
  img.style.top = "0px";
  var clip = (new zoyoe.game.clip(name,ele));
  clip.para = para;
  clip.type = game.actortype.GENERAL_MONSTER;
  game.actor.BuildMoveAction(clip);
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
          cell.zidx(r * cells.length + l);
        }
      }
    }
    inst.initStage(this.clip);
  };
  this.instance = inst;
  this.clip = clip;
}

