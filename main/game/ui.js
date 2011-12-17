function ZOYOE_UI(env,ajax,support,interface){
  var _dialog_html = "
    <div id='dialog'>
     <div class='dialog'>
      <div class='dialog-hint'><a></a>
      </div>
      <div class='dialog-content'>
      </div>
      <div class='button-lane'>
      </div>
     </div>
    </div>
  "

  /* All the helper functions that was used in zoyoe.ui */
  var _I = interface;
  /* This is the interface that for 
  function html = function(a,ht){
     if(support =="YUI"){
       a.set('innerHTML',ht);
     }else if(support == "JQUERY"){
       a.html(ht);
     }
  }
  function css = function(a,cn,cs){
     if(support =="YUI"){
       a.setStyle(cs,cn);
     }else if(support == "JQUERY"){
       a.css(cs,cn);
     }
  }
  function select = function(cstring){
     if(support =="YUI"){
       return I.one(cstring); 
     }else if(support == "JQUERY"){
       return I(cstring);
     }
  }
  function dom = function(supportele){
     if(support =="YUI"){
       return I.Node.getDOMNode(supportele);
     }else if(support == "JQUERY"){
       return supportele.get(0); 
     }
  }
  function dialog(form,title,hint,content,submit,callback){
    this.form = form;
    this.title = title;
    this.hint = hint;
    this.status = 'prepare';
    this.content = content;
    this.submit = submit;
    this.callback = callback;
  }

  var _dialogs = [];
  var _pending_dialog = null;
  this.dialog = select('#dialog');
  this.PopDialog = function(info){
    var dialog = dialogs.pop();
    html(select('#dialog .dialog-hint'),dialog.hint);
    if(form){
      dom(select('#dialog .dialog-content')).appendChild(form);
    }else{
      html(select('#dialog .dialog-content'),dialog.content.get());
    }
  }
  this.DialogSubmit = function(){
    //var dialog = select('#dialog .dialog-content');
    //var hint = select('#dialog .dialog-hint');
    html(hint,"<a></a><h2></h2>");
    var dialog = dialogs.pop();
    if(dialog.submit){
      _pending_dialog = dialog;
      dialog.submit();
      return; /* Leave the callback function to do stuff */
    }else{
    /* if this is the last dialog in the queue */
      if(_dialogs.length == 0){
        css(this.dialog,'display','none');
        this.ActivateContent();
      }else{
        html(select('#dialog'),_dialog_html);
        this.PopDialog();
      }
    }
  }
  this.PrepareDialog = function(content,dialog){
    di
    content.ready(function(data)){
    });
  }
  this.ShowDialog = 
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


  var YUI = yui;
  var ENV = env; 
  var UI = this;
  /* UI Component *,ajax/
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
  this.replydata = null;
  this.update = null;
  this.complete = null;
  this.dialog_title = null;
  this.dialog_name = null;
  this.static_dialog = static_dialog;
  this.dialog_commit_btn = this.dialog.one(".button-lane input.commit");
  this.dialog_cancel_btn = this.dialog.one(".button-lane input.cancel");
  this.panel_name = null;
  this.panel = YUI.one("#panel")


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
 function StartIO(uri,config,call_back,paras){
    var sub = YUI.on('io:complete',function(id,o,args){
      call_back(id,o,args);
      sub.detach();
    },YUI,paras);
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
      if(data && data.documentElement){
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
         UI.refresh = refresh;
         UI.replydata = data;
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
  function LoadContent(content,uri){
    function complete(id,o,args){
      var data = o.responseText;
      ENV.ALERT(o.responseText);
      content.one('div.panel-content').set("innerHTML",data);
    }
    var config = {
      method: 'get',
    }
    StartIO(uri,config,complete);
  }
  this.LoadFrameForm = function(uri){
    function complete(id,o,args){
      var data = o.responseText;
      ENV.ALERT(o.responseText);
      var btnlane = YUI.one('#panel .panel-left');
      btnlane.set("innerHTML",data);
    }
    var config = {
      method: 'get',
    }
    StartIO(uri,config,complete);
  }
  this.ClearButtons = function(){
    var btn_lane = YUI.one('#panel .button-lane');
    btn_lane.set("innerHTML","");
  }
  this.LoadButton = function(str,callback){
    var btn_lane = YUI.one('#panel .button-lane');
    ele = YUI.Node.create("<input type='button' value='"+str+"'></input>"); 
    ele.on('click',callback);
    btn_lane.append(ele);
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
                method: 'get',
              }
              var p = YUI.one("#"+UI.update.comp_id).get('parentNode');
              p.set('innerHTML','loading');
              function complete(id,o,args){
                zoyoe.ALERT(o.responseText);
                p.set('innerHTML',o.responseText);
                UI.update = null;
                UI.HideDialog();
                if(zoyoe.ElementExtension){
                  zoyoe.ElementExtension.BuildExtensionElements(p);
                }
              }
              StartIO(UI.update.uri,config,complete);
            }else if(UI.update.uri){
              ENV.Redirect(UI.update.uri);
            }else if(typeof(UI.update) == "function"){
              UI.update(UI.replydata);
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
  this.ShowPanel = function(panel_name,args){
  /* Currently only two kinds of panel is supported
   * 1. Gallery Panel (Resource Panel)
   * 2. Data Panel
   */
  
  /* First Of All, Hibernate the content */
    this.HibernateContent();

  /* Prepare the content */
  var panel = YUI.one('#panel .panel-content');
  var hint = YUI.one('#panel .panel-hint');
  var btnlane = YUI.one('#panel .button-lane');
  var pleft = YUI.one('#panel .panel-left');

  /* Clear The Content */
  btnlane.set("innerHTML","");
  pleft.set("innerHTML","");
  panel.set("innerHTML","");
  if(panel_name == "gallery"){
    var gname = args[0];
    var icon9 = "";
    for (var i=0;i<9;i++){
      icon9 += "<a onclick=\"zoyoe.comps['GALLERY'].Select("+i+",this)\" class='gicon'></a>"
    };
    pleft.set("innerHTML",icon9);
    var tstamp = "";
    if(ENV){
      tstamp = "&tstamp="+ENV.TimeStamp();
    }
    /* The Uri Where We Get The Photo Data */
    var info_uri = "/core/gallery/"+ENV.service_name+"/?" + tstamp;
    function complete(io,o,args){
      var icon_containers = UI.panel.all(' .gicon')
      var gs = o.responseXML.getElementsByTagName('G');
      var g = null;
      gname = args[0]; 
      for (var i=0;i<gs.length;i++){
        if(gs[i].getAttribute('name') == gname){
          g = gs[i];
        }
      }
      if(g == null){return;}
      else{
        var urls = g.getElementsByTagName('IMG'); 
        var gname = g.getAttribute('name');
        var prefix = "/core/data/res/"+ENV.service_name+"/"+gname;
        var idx = 0;
        var name_list = [];
        for(;idx<7&&idx<urls.length;idx++){
          var name = urls[idx].getAttribute('name');
          icon_containers.item(idx).set('innerHTML',
            "<img src='"
            +prefix + '/' + name + "/?sc=small" + tstamp + "'></img>");
          name_list.push(name);
        }
        for(var i = idx;i<9;i++){
          icon_containers.item(i).set('innerHTML','');
        }
        zoyoe.comps['GALLERY'].ManageGallery(gname,name_list,function(innerHTML){
          panel.set('innerHTML',innerHTML);
        });
      }
    }
    var config = {
      method: 'GET',
    }
    StartIO(info_uri,config,complete,[gname]);
    var ghint = "<a class='gbutton' onclick='zoyoe.ui.HidePanel()'>&#9746</a>"
                   + "<h2>Gallery:"+gname+"</h2>"
    hint.set('innerHTML',ghint);
    this.LoadButton("Del Gallery",function(){zoyoe.ui.HidePanel();zoyoe.comps['GALLERY'].DelGallery(gname);});
    this.LoadButton("Create New",function(){zoyoe.comps['GALLERY'].AddImg()});
    this.LoadButton("Modify Current",function(){zoyoe.comps['GALLERY'].ModifyImg(gname);});
    YUI.one('#panel').setStyle('display','block');
  }else if(panel_name == "data"){
    this.panel_name = "data";
    var path = args.path; /* convension used here */ 
    var render_uri = "/xml/rend/"+ENV.service_name+"/"+path+"/";
    var add_uri = "/xml/add/"+ENV.service_name+"/"+path+"/";
    var ghint = "<a class='gbutton' onclick='zoyoe.ui.HidePanel()'>&#9746</a>"
                 + "<h2>DataPanel: "+path+"</h2>"
    hint.set('innerHTML',ghint);
    LoadContent(UI.panel,render_uri);
    YUI.one('#panel').setStyle('display','block');
  }else{
    alert("fatal error");
    UI.ActivateContent();
    return;
  }
 }
 this.PanelFormSubmit =function (uri,config,left_ref,right_ref){
  function complete(id,o,args){
    if(left_ref){
      UI.panel.one('div.panel-left').set("innerHTML",o.responseText);
    }
    if(right_ref){
      var render_uri = "/xml/rend/"+ENV.service_name+"/"+right_ref+"/";
      LoadContent(UI.panel,render_uri);
    }
  }
  StartIO(uri,config,complete);
 }

 this.HidePanel = function(){
   UI.panel.setStyle('display','none');
   UI.ActivateContent();
 }
}
