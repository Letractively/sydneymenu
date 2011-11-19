var MOTION = new function(){
	this.NULL = 0;
	this.TRANSLATION = 1;
};
function n2px(n){
  return n+"px";
}
zoyoe = {};

zoyoe.PAUSE = 1;
zoyoe.RUN = 0;
 
zoyoe.noopFrame = function(parent,idx){
	var index = idx;
	var clip = parent;
	var iskeyframe = false;
	var clips = {};
    var status = zoyoe.RUN;
    this.tracked = function(c){
      if(clips[c.name()]){
        return true;
      }else{
        return false;
      }
    }
    this.getTrack = function(name){
      return clips[name];
    }
	this.getIndex = function(){
		return index;
	};
	this.getClips = function(){
		return clips;
	};
	this.trackClip = function(clip){
        if(clips[clip.name()]!=undefined){
          return clips[clip.name()];
        }else{
		  clips[clip.name()] = new zoyoe.clipprox(clip);
		  iskeyframe = true;
          return clips[clip.name()];
        }
	};
	this.keyframe = function (){
		return iskeyframe;
	};
    this.clips = function(){
        return clips;
    }
    this.action = function(cb){
        return;
    }
	this.render = function(){
		if(iskeyframe){
			for(c in clips){
                clips[c].action();
				clips[c].clip.position(clips[c].top,clips[c].left);
			}
		}else{
          var pk = clip.getPreKey(index);
          var nk = clip.getNextKey(index);
          if(pk && nk){
			var pcs = pk.clips();
			var ncs = nk.clips();
			for (var key in pcs){
              var pc = pcs[key];
              var nc = ncs[key];
              if(nc){
                switch(pc.motion){
                case MOTION.TRANSLATION:
                  var lambda = (this.getIndex()-pk.getIndex())/(nk.getIndex()-pk.getIndex());
                  var top = pc.top*(1-lambda) + nc.top*lambda;
                  var left = pc.left*(1-lambda) + nc.left*lambda;
                  pc.clip.position(top,left);
				break;
				}
			  }
		    }
	      }
        }
	/* It is not implemented well */
	};
};
zoyoe.clip = function (n,ele,top,left){
  var relative_top = 0;
  var relative_left = 0;
  var element = ele;
  var clips = [];
  var frames = [new zoyoe.noopFrame(this,0)];
  var idx = 0;
  var name = n;
  var status = zoyoe.RUN;
  ele.id = n;
  if(!isNaN(top)){
    relative_top = top;
  }
  if(!isNaN(left)){
    relative_left = left;
  }
  this.reset = function(){
    element.innerHTML = "";
    clips = [];
    frames = [new zoyoe.noopFrame(this,0)];
    idx = 0;
    status = zoyoe.RUN;
  }
  this.clips = function(){
	  return clips;
  };
  this.element = function(){
    return element;
  }
  this.getPreKey = function(idx){
	  for(var i = idx;0<=i;i--){
		  if(frames[i].keyframe()){
			  return frames[i];
		  }
	  };
	  return null;
  };
  this.getNextKey = function(idx){
	  for(var i = idx+1;i<frames.length;i++){
		  if(frames[i].keyframe()){
			  return frames[i];
		  }
	  };
	  return null;
  };
  this.position = function(top,left){
	  if((!isNaN(top))&&(!isNaN(left))){
		  relative_top = top;
		  relative_left = left;
	  }
	  return {top:relative_top,left:relative_left};
  };
  this.render = function(){
    element.style.top = n2px(relative_top); 
    element.style.left = n2px(relative_left); 
  };
  this.inc = function(){
	  idx = idx+1;
	  if(idx == frames.length){
		  idx = 0;
	  }
  };
  this.setCallBack = function(frame_idx,callback){
	  if(frame_idx<frames.length){
		  throw "frame idx overflow";
	  }else{
		  this.frames[frame_idx.callbac = callback];
	  }
  };
  this.step = function(){
    if(status == zoyoe.RUN){
	  var frame = frames[idx];
	  frame.render(this);
      var keyframe = this.getPreKey(idx);
      for(var c in clips){
        if(keyframe.tracked(clips[c])){
		  clips[c].step();
          if(clips[c].element().parentNode == element){
            /* don know what to do here */
          }else{
            element.appendChild(clips[c].element());
          } 
        }else{
          try {
            element.removeChild(clips[c].element());
          }catch(exception) {
            /* pass silently here */
          }
        }
      }
      this.render();
      this.inc();
    }else{
      alert(name+" not running");
    }
  };
  this.play = function(){
    status = zoyoe.RUN;
  };
  this.stop = function(){
    status = zoyoe.PAUSE;
  };
  this.gotoAndPlay = function(){
    /* not implemented */
  };
  this.insertClip = function(clip){
	  this.clips().push(clip);
  };
  this.name = function(){
    return name;
  };
  this.trackClip = function(keyframe,clip){
    return keyframe.trackClip(clip);
  };
  this.appendFrames = function(n){
    var start = frames.length;
    for(var i=0;i<n;i++){
      frames.push(new zoyoe.noopFrame(this,start+i));
    }
    return start;
  };
  this.getFrame = function(n){
    return frames[n];
  }
  this.top = function(){
    return relative_top;
  }
  this.left = function(){
    return relative_left;
  }
}
zoyoe.clipprox = function(clip){
	this.clip = clip;
	this.top = clip.top();
	this.left = clip.left();
	this.motion = MOTION.NULL;
    this.action = function(){
      return;
    }
}

zoyoe.newName = function(){
  if(!zoyoe.ninc){
    zoyoe.ninc = 0;
  }
  var name = "zoyoe_name_gen_"+zoyoe.ninc;
  zoyoe.ninc ++;
  return name;
}
 
zoyoe.env = function(ele,fps,top,left){
  var delaywindow = 1000/fps;
  var status = zoyoe.PAUSE;
  var topclip = new zoyoe.clip('root',ele,top,left);
  var topele = ele;
  var self = this;
  var timer = null;
  this.step = function(){
	  topclip.step();
  };
  this.root = function(){
      return topclip;
  };
  this.reset = function(){
      window.clearTimeout(timer);
      status = zoyoe.PAUSE;
      topclip.reset();
  };
  this.run = function(){
    status = zoyoe.RUN;
    this.step();
    timer = window.setTimeout(function(){
      if(status == zoyoe.RUN){
          self.run();
      }else{
          return;
      }		
    },delaywindow);	
  }
};
