function ZOYOE_UI(env,yui,static_dialog){
  var YUI = yui;
  var ENV = env; 
  var UI = this;
  /* UI Component */
  this.right_dock = null;
  this.left_dock = null;
  this.content = null; 
  this.top_dock = null;
  this.bot_dock = null;
  this.hibernate_count = 0;
  this.content_active = true;
  this.submit_cb = null;
  this.refresh = false;
  this.dialog = YUI.one('#dialog');
  this.update = null;
  this.complete = null;
  this.dialog_title = null;
  this.static_dialog = static_dialog;
  this.dialog_commit_btn = this.dialog.one(".button-lane input.commit");
  this.dialog_cancel_btn = this.dialog.one(".button-lane input.cancel");


  function DialogStyleCommit(){
    UI.dialog_commit_btn.set('value',"continue");
    UI.dialog_cancel_btn.set('value',"cancel");
    UI.dialog_cancel_btn.setStyle('display',"");
  }

  function DialogStyleAlert(){
    UI.dialog_commit_btn.set('value',"ok");
    UI.dialog_cancel_btn.set('value',"cancel");
    UI.dialog_cancel_btn.setStyle('display',"");
  }

  function DialogStyleSucc(){
    UI.dialog_commit_btn.set('value',"ok");
    UI.dialog_cancel_btn.set('value',"cancel");
    UI.dialog_cancel_btn.setStyle('display',"none");
  }

  /* Set the complete function */
  YUI.on('io:complete',function(id,o,args){
    UI.complete(id,o,args)
  });
  function StartIO(uri,config,call_back){
    UI.complete = call_back;
    var request = YUI.io(uri,config);
  }
  function BuildGeneralMsg(msg,url,error_hint){
    var title = YUI.one('#dialog .dialog-hint h2');
    var hint = YUI.one('#dialog .dialog-hint a');
    var dialog = YUI.one('#dialog .dialog-content');
    if(error_hint){
      hint.set('innerHTML',"<img src = '/res/alert-icon.png'/>" + error_hint);
    }
    dialog.set('innerHTML',"<div class='msg'>"+msg+"</div>");
    UI.submit_cb = null;
  }

  function BuildSuccMsg(msg,url){
    var title = YUI.one('#dialog .dialog-hint h2');
    var hint = YUI.one('#dialog .dialog-hint a');
    var dialog = YUI.one('#dialog .dialog-content');
    dialog.set('innerHTML',msg);
    hint.set('innerHTML',"");
    UI.submit_cb = null;
  }
  
  function BuildErrorMsg(msg,url){
    var hint = YUI.one('#dialog .dialog-hint a');
    var url = url;
    if(url == null){
      url = "";
    }
    hint.set('innerHTML',"<img src = '/res/alert-icon.png'/>" + msg);
  }
  function ClearHint(){
    var hint = YUI.one('#dialog .dialog-hint a');
    hint.set('innerHTML',"");
  }

  this.BuildGeneralMsg = BuildGeneralMsg;
  this.BuildSuccMsg = BuildSuccMsg;
  this.BuildErrorMsg = BuildErrorMsg;
  this.HideDialog = function(){
    var dialog = YUI.one('#dialog .dialog-content');
    var hint = YUI.one('#dialog .dialog-hint');
    hint.set('innerHTML',"<a></a><h2></h2>");
    if(UI.static_dialog != true){
      YUI.one('#dialog').setStyle('display','none');
      this.ActivateContent();
    }
  }
  this.ShowDialog = function(title,loading){
    if(UI.static_dialog != true){
      this.HibernateContent();
      YUI.one('#dialog').setStyle('display','block');
    }
    var hint = YUI.one('#dialog .dialog-hint');
    var ghint = "<a></a><h2>" + title + "</h2>";
    UI.dialog_title = title;
    hint.set('innerHTML',ghint);
    if(loading){
      var dialog = YUI.one('#dialog .dialog-hint a');
      dialog.set('innerHTML',"loading ...");
    }
  }
  /* Alert Dialog, Ask you to confirm your action */
  this.GeneralAlert = function(msg,hint,call_back,refresh){
    this.ShowDialog('Alert',false)
    DialogStyleAlert();
    UI.BuildGeneralMsg(msg,null,hint);
    this.submit_cb = call_back;
    this.refresh = refresh;
  }
  /* ResopnseDialog which is not triggered by a info_collect dialog*/
  this.ResponseDialog = function(uri,config,refresh,info){
    /* uri: the request uri you will post or get
       config: the yui io config 
       refresh: whether refresh the page(whole or partially)
       info: information about how to refresh the page
    */
    this.ShowDialog('Response',true);
    DialogStyleSucc();
    function complete(id,o,args){
      ClearHint();
      env.ALERT(o.responseText);
      var data = o.responseXML;
      if(data){
        if(data.documentElement.tagName == 'SUCC'){
          var msg = data.documentElement.getElementsByTagName('HTMLMSG')[0].firstChild.data;
          UI.BuildGeneralMsg(msg,null);
          UI.refresh = true;
          UI.update = info;
        }else{ /* An Error has occurred */
          var msg = data.documentElement.getElementsByTagName('HTMLMSG')[0].firstChild.data;
          var errors = data.documentElement.getElementsByTagName('ERROR');
         if(errors.length > 0 ){
            var fst_error = errors[0].firstChild.data;
            msg = msg+fst_error;
            UI.BuildGeneralMsg(msg,null,fst_error);
          }else{
            UI.BuildGeneralMsg(msg);
          }
        }
      }else{
         UI.BuildGeneralMsg(o.responseText);
      }
    }
    StartIO(uri,config,complete);
  }
  /* This is used eto handle the result of a info_colloect dialog */
  this.GeneralDialogCont = function(uri,config,refresh,info){
    this.ShowDialog(UI.dialog_title,true);
    function complete(id,o,args){
      ClearHint();
      var data = o.responseXML;
      ENV.ALERT(o.responseText);
      if(data){
        if(data.documentElement.tagName == 'SUCC'){
         var msg = data.documentElement.getElementsByTagName('HTMLMSG')[0].firstChild.data;
         BuildGeneralMsg(msg,null);
         UI.refresh = true;
         UI.update = info;
         DialogStyleSucc();
        }else{
          var errors = data.documentElement.getElementsByTagName('ERROR');
          if(errors.length > 0 ){
            var fst_error = errors[0].firstChild.data;
            ENV.ALERT(fst_error);
            UI.BuildErrorMsg(fst_error);
          }
          else{
            UI.BuildErrorMsg('UNKOW ERROR!!');
          }
          var error_nodes = YUI.all('#' + UI.dialog_name + ' .input-error');
          error_nodes.replaceClass('input-error','input-fine');
          for (var i=0;i<errors.length;i++){
            var name = errors[i].getAttribute('name');
            var path = "#" + UI.dialog_name + " #"+name+' .input-fine';
            var anode = YUI.one(path);
            if(anode){
              anode.replaceClass('input-fine','input-error');
            } 
          }
        }
      }else{
         UI.BuildGeneralMsg(o.responseText);
      }
    }
    StartIO(uri,config,complete);
  }
  this.InfoCollectDialog = function(h,uri,dialog_name,submit_callback,init_callback){
    DialogStyleCommit();
    this.ShowDialog(h,true);
    this.submit_cb = submit_callback;
    this.dialog_name = dialog_name;
    function complete(io,o,args){
      ClearHint();
      var msg = o.responseText+" ";
      var d = YUI.one('#dialog .dialog-content');
      var dialog_ele = YUI.Node.getDOMNode(d);
      dialog_ele.innerHTML = msg;
      if(ENV.ElementExtension){
        ENV.ElementExtension.BuildExtensionElements(d);
      }
      if(init_callback){
        init_callback(YUI.one("#dialog"));
      }
      DialogStyleCommit();
    } 
    StartIO(uri,config,complete);
  }
  this.IframeDialog = function(h,uri,dialog_name,submit_callback){
    this.ShowDialog(h,false);
    this.submit_cb = submit_callback;
    this.dialog_name = dialog_name;
    var dialog = YUI.one('#dialog .dialog-content');
    var ht = "<iframe frameborder='0' id='"+dialog_name + "' src = '"+uri+"'></iframe>"
    dialog.set('innerHTML',ht);
  }
  this.HibernateContent = function(no_opacity){
    /* We will not check the existance of the mask, 
    since we can not handle the problem once the convention is not applied */
    this.hibernate_count += 1;
    if(this.hibernate_count == 1){
      var mask = document.getElementById('zsk');
      if(no_opacity){
        mask.className = 'msk_nop';
      }else{
        mask.className = 'msk';
      }
      mask.style.display = 'block';
      this.content_active = false;
    }
  }
  this.ActivateContent = function(){
    this.hibernate_count -= 1;
    if(this.hibernate_count < 0){
      alert("fail");
    }
    if(this.hibernate_count == 0){
      var mask = document.getElementById('zsk');
      mask.style.display = 'none';
      document.body.style.overflow = "";
      this.content_active = true;
    }
  }

  this.InputKeydownListener = function(event) {
      switch(event.keyCode) {
      case 13: 
        UI.SubmitForm();
        break;
      case 27:
        UI.HideDialog();
        break;
      default:
        break;
      }
  }
  this.SubmitForm = function(){
    var form_obj = document.getElementById(UI.dialog_name);
    if(form_obj!=null){
      if(UI.submit_cb){
        UI.HideDialog();
        UI.submit_cb(form_obj);
      }else{
        UI.HideDialog();
      } 
    }else{
      if(UI.submit_cb){
        UI.HideDialog();
        UI.submit_cb();
      }else{
        if(UI.refresh){
          if(UI.update){
            if(UI.update.comp_id){
              var config = {
                method: 'GET',
              }
              var p = document.getElementById(UI.update.comp_id).parentNode;
              p.innerHTML = 'loading';
              function complete(id,o,args){
                zoyoe.ALERT(o.responseText);
                p.innerHTML = o.responseText;
                UI.update = null;
                UI.HideDialog();
              }
              StartIO(UI.update.uri,config,complete);
            }else{
              ENV.Redirect(UI.update.uri);
            }
          }else{
            location.reload(true); 
          }
        }else{
          UI.HideDialog();
        }
      }
    }
  }
}
