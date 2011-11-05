function update_info(uri,comp_id){
  this.uri = uri;
  this.comp_id = comp_id;
}
function InitIcon(env){
  var icon = new function(){
    this.content_setter = null;
    this.modify_uri = function(){
      return "/core/imagelink/" + env.service_name + "/icon/";
    }
    this.update_icon = function(){
      return "/core/service/" + env.service_name + "/?comp=icon"
    }
    this.ModifyIcon = function(){
      var src = "/core/dialog/modifyres/"
                + env.service_name
                + "/icon/?quick=true"
      var self = this;
      env.ui.IframeDialog('Icon',src,'iframe_change_icon',function(iframe){
        self.ModifyIconProgress(iframe);
      });
    }
    this.ModifyIconProgress = function(iframe){
      var config = {
        method: 'GET',
      }
      var doc = iframe.contentWindow || iframe.contentDocument;
      doc = doc.document;
      if(doc && doc.zoyoe && doc.zoyoe.dialog=='complete'){
        env.ui.ResponseDialog(this.modify_uri(),config,true
          ,new update_info(this.update_icon(),"icon"));
      }else{
         //env.ALERT(doc.zoyoe.dialog);
      }
    }
  }
  return icon;
}
function InitLayout(env){
  function getSection(node){
    if(node.className=='section-container'){
      var section = null;
      for(var c = node.firstChild;c;c=c.nextSibling){
        if(c.className=='section'){
          env.ALERT(c.id);
          section = c;
          break;
        }
      }
      return section;
    }else{
      return null;
    }
  }
  var layout = new function(){
    this.info = null;
    this.save_uri = function(){
      return "/core/layout/"+env.service_name+'/save/';
    }
    this.build_layout = function(section_name){
      var section_str = [];
      var section = document.getElementById(section_name);
      for(var c = section.firstChild;c;c=c.nextSibling){
        var s = getSection(c);
        if(s){
          section_str.push(s.id);
        }
      }
      return section_str.join(','); 
    }
    this.SaveLayout = function(){
      var config = {
        method: 'GET',
        data:   'left='   + this.build_layout('left-section')
              + "&middle="+ this.build_layout('mid-section')
              + "&right=" + this.build_layout('right-section')
      }
      var request = env.ui.ResponseDialog(this.save_uri(),config,true,null);
        //,new update_info(this.update_uri(),""));
    }
  }
  return layout;
}

function InitRoster(env,day){
  function InfoCache(day,select){
    this.day = day;
    this.select = select;
  }
  var roster_comp = new function(){
    this.cache = null;
    this.info_cache = new InfoCache(day,null);
    this.add_roster_uri = function(){
      return "/core/roster/"+env.service_name+'/add/'+this.info_cache.day;
    }
    this.del_roster_uri = function(){
      return "/core/roster/"+env.service_name+'/remove/'+this.info_cache.day;
    }
    this.dialog_add_uri = function(){
      return "/core/dialog/addroster/"+env.service_name+'/'+this.info_cache.day;
    }
    this.update_uri = function(){
      return "/core/service/" + env.service_name +"/?comp=roster&day="+this.info_cache.day;
    }
    this.Select = function(info,ele){
      if(this.cache == ele && ele.className == 'select'){
        ele.className='';
        this.info_cache.select = null;
        this.cache = null;
      }else{
        if(this.cache){
          this.cache.className='';
        }
        ele.className='select';
        this.cache = ele;
        this.info_cache.select = info;
      }
    }
    this.ShowAddDialog = function(){
      var self = this;
      env.ui.InfoCollectDialog("Add Roster",
        self.dialog_add_uri(), 
        "form-addroster",
        function(form_obj){
          self.AddRoster(form_obj)
        }
      );
    }
    this.Update = function(day){
      this.info_cache.day = day;
      this.info_cache.select = null;
      env.Update(new update_info(this.update_uri(),"roster"));
    }
    this.AddRoster = function(form_obj){
      var config = {
        method: 'GET',
        form: {id:form_obj}
      }
      var uri = this.add_roster_uri();
      var request = env.ui.GeneralDialogCont(uri,config,true
        ,new update_info(this.update_uri(),"roster"));
    }
    this.DelRoster = function(gname){
      var config = {
        method: 'GET',
        data:'name='+gname
      }
      var uri = this.del_roster_uri();
      var request = env.ui.ResponseDialog(uri,config,true
        ,new update_info(this.update_uri(),"roster"));
    }
    this.DelSelect = function(){
      if(this.info_cache.select){
        this.DelRoster(this.info_cache.select);
      }
    }
  }
  return roster_comp;
}

function InitItems(env,p){
  var item_comp = new function(){
    var path = p;
    this.cache = null;
    this.info_cache = null;
    this.form_name = "xsd-"+path+"-form";
    this.form_uri = function(info){
      if(info  && 0 <= info){
        return "/xml/dialog/xsd/"+zoyoe.service_name+"/" + path + "/?id="+info;
      }else{
        return "/xml/dialog/xsd/"+zoyoe.service_name+"/" + path + "/";
      }
    }
    this.add_uri = function(){
      return "/xml/add/"+env.service_name+'/' + path + '/';
    }
    this.modify_uri = function(id){
      return "/xml/modify/"+env.service_name+'/' + path + '/?id='+id;
    }
    this.delete_uri = function(id){
      return "/xml/remove/"+env.service_name+'/'+id+"/";
    }
 
    this.Select = function(info,ele){
      if(this.cache == ele && ele.className == 'select'){
        ele.className='datalane';
        this.info_cache = null;
        this.cache = null;
        zoyoe.ui.DisableFrameForm();
      }else{
        if(this.cache){
          this.cache.className='datalane';
        }
        ele.className='select';
        this.cache = ele;
        this.info_cache = info;
        zoyoe.ui.ClearButtons();
        zoyoe.ui.LoadFrameForm(this.form_uri(info));
        if(info == -1){
          zoyoe.ui.LoadButton("Commit",function(){
            item_comp.AddItem();
          });
        }else{
          zoyoe.ui.LoadButton("Save",function(){
            item_comp.ModifyItem();
          });
          zoyoe.ui.LoadButton("Delete",function(){
            item_comp.DeleteItem();
          });
        }
      }
    }
    this.ModifyItem = function(dbid){
      var config = {
        method: 'GET',
        form: {id:item_comp.form_name}
      }
      var uri = this.modify_uri(this.info_cache);
      var request = env.ui.PanelFormSubmit(uri,config,true,path)
    }
    this.AddItem = function(){
      var config = {
        method: 'GET',
        form: {id:item_comp.form_name}
      }
      var uri = this.add_uri();
      var request = env.ui.PanelFormSubmit(uri,config,true,path)
    }
    this.DeleteItem = function(){
      var config = {
         method: 'GET',
      }
      var uri = this.delete_uri(this.info_cache);
      var request = env.ui.PanelFormSubmit(uri,config,true,path)
    }
    this.ShowModifyDialog = function(){
      zoyoe.ui.ShowPanel('data',{path:path});
    }
  }
  return item_comp;
}

function InitGallery(env){
  function IHandler(name,ele){
    this.name = name;
    this.ele = ele;
  }
  var gallery_comp = new function(){
    this.cache = null;/* The current focus element */
    this.info_cache = null; /* The current Select image item */
    this.showing_gallery = null;
    this.image_handler = [];
    this.content_setter = null;
    this.del_gallery_uri = function(){
      return "/core/gallery/"+env.service_name+'/remove/';
    }
    this.add_gallery_uri = function(){
      return "/core/gallery/"+env.service_name+'/add/';
    }
    this.dialog_add_uri = function(){
      return "/core/dialog/addgallery/"+env.service_name;
    }
    this.Select = function(idx,ele){
     if(idx<this.image_handler.length){
        this.content_setter("<img src='/core/data/res/"
          +    env.service_name
          +"/" + this.showing_gallery
          +"/" + this.image_handler[idx].name+"'></img>"); 
        this.info_cache = idx;
        this.cache = ele;
      }else{
        return;
      }
    }
    this.AddGallery = function(form_obj){
      var config = {
         method: 'GET',
         form: {id:form_obj}
      }
      var uri = this.add_gallery_uri();
      var request = env.ui.GeneralDialogCont(uri,config,true
        ,new update_info("/core/service/"+env.service_name+"/?comp=gallery","gallery"));
    }
    this.DelGallery = function(gname){
      var config = {
         method: 'GET',
      }
      var uri = this.del_gallery_uri() + gname;
      var request = env.ui.ResponseDialog(uri,config,true
        ,new update_info("/core/service/"+env.service_name+"/?comp=gallery","gallery"));
    }
    this.ShowAddDialog = function(){
      var self = this;
      env.ui.InfoCollectDialog("Add Gallery",
        self.dialog_add_uri(), 
        "form-addgallery",
        function(form_obj){
          self.AddGallery(form_obj)
        }
      );
    }
    this.ManageGallery = function(gname,name_list,setter){
      this.showing_gallery = gname;
      this.content_setter = setter;
      this.image_handler = [];
      for(var i=0;i<name_list.length;i++){
        this.image_handler.push(new IHandler(name_list[i]))
      }
      if(name_list.length == 0){
      this.content_setter("<h1>Oops!!! This Gallery is Empty at the Moment. </h1>"
        + "<p>For information about how to manage the gallery please visit our help page</p>"
        + "<br/> <p>To add a new image click button 'update new image'</p>"
        + "<br/> <p>To delete this gallery click button 'delete this gallery'</p>")
      }
    }
    this.AddImg = function(){
      if(this.showing_gallery == null){
      }else if(this.image_handler.length==9){
        this.content_setter("<h1>Oops!!! This Gallery is Full at the Moment. </h1>"
          + "<p>For information about how to manage the gallery please visit our help page</p>"
          + "<br/> <p>To delete this gallery click button 'delete this gallery'</p>")
      }else{
        var ht = "<iframe onload=\"zoyoe.comps['GALLERY'].AddImgProgress(this," + this.image_handler.length + ")\" src = '/core/dialog/addres/"
                + env.service_name
                + "/" + this.showing_gallery
                + "/photo" + this.image_handler.length +"' ></iframe>"
        this.content_setter(ht);
      }
    }
    this.ModifyImg = function(){
      if(this.showing_gallery == null){
      }else if(this.info_cache == null){
      }else{
        var ht = "<iframe onload=\"zoyoe.comps['GALLERY'].ModifyImgProgress(this," + this.info_cache + ")\" src = '/core/dialog/modifyres/"
                + env.service_name
                + "/" + this.showing_gallery
                + "/photo" + (this.info_cache) +"' ></iframe>"
        this.content_setter(ht);
      }
    }
    this.AddImgProgress = function(iframe,length){
      var doc = iframe.contentWindow || iframe.contentDocument;
      var SUCC = doc.document.getElementsByTagName('SUCC');
      if(SUCC.length == 1){
        env.timestamp = SUCC[0].getAttribute('timestamp');
        //Convention Used Here
        this.content_setter("<img src='/core/data/res/"
          +    env.service_name
          +"/" + this.showing_gallery
          +"/photo" + length+"'></img>"); 
        //alert(SUCC[0].getElementsByTagName('HTMLMSG')[0].firstChild.data);
        //Update Component
        env.ui.HidePanel();
        env.ui.ShowPanel('gallery',[this.showing_gallery]);
      }
    }
    this.ModifyImgProgress = function(iframe,length){
      var doc = iframe.contentWindow || iframe.contentDocument;
      var SUCC = doc.document.getElementsByTagName('SUCC');
      if(SUCC.length == 1){
        env.timestamp = SUCC[0].getAttribute('timestamp');
        //Convention Used Here
        this.content_setter("<img src='/core/data/res/"
          +    env.service_name
          +"/" + this.showing_gallery
          +"/photo" + length+"'></img>"); 
        //alert(SUCC[0].getElementsByTagName('HTMLMSG')[0].firstChild.data);
        //Update Component
        env.ui.HidePanel();
        env.ui.ShowPanel('gallery',[this.showing_gallery]);
      }
    }
  }
  return gallery_comp;
}
function InitBasicInfo(zo){
  var env = zo;  
  var basic_info = new function(){
    this.mdy_dialog_uri = "/core/dialog/mdyservice/";
    this.mdy_service_uri = "/core/data/mdyservice/";
    this.ShowModifyServiceDialog = function(){
      var uri = this.mdy_service_uri;
      function ModifyService(form_obj){
        var days = new Array();
        if(form_obj.Sun.checked){days.push("Sun");}
        if(form_obj.Mon.checked){days.push("Mon");}
        if(form_obj.Tue.checked){days.push("Tue");}
        if(form_obj.Wed.checked){days.push("Wed");}
        if(form_obj.Thu.checked){days.push("Thu");}
        if(form_obj.Fri.checked){days.push("Fri");}
        if(form_obj.Sat.checked){days.push("Sat");}
        zoyoe.ALERT(days.join(','));
        var mdy_service_config = {
          method: 'POST',
          data:"&days="+days.join(','),
          form: {id:form_obj}
        }
        zoyoe.ui.GeneralDialogCont(uri+zoyoe.service_name+"/",mdy_service_config,true,null);
      }
      env.ui.InfoCollectDialog("BasicInfo",
      this.mdy_dialog_uri,"form-mdyservice",ModifyService);
    }
  }
  return basic_info;
}
function InitAdmin(zo){
  var env = zo;
  var admin = new function(){
    this.login_uri = "/core/user/login/";
    this.register_uri = "/core/user/register/";
    this.change_pwd_uri = "/core/user/changepwd/";
    this.addserv_dialog_uri = "/core/dialog/addservice/";
    this.login_dialog_uri = "/core/dialog/login/";
    this.register_dialog_uri = "/core/dialog/register/";
    this.pwd_dialog_uri = "/core/dialog/changepwd/";
    this.del_uri = function(sname){
      return "/core/data/delservice/"+sname+"/";
    }
    this.reset_uri = function(sname){
      return "/core/data/reset/"+sname+"/";
    }
    this.enable_forum_uri = function(sname){
      return "/glue/forum-activate/"+sname+"/";
    }
    this.DeleteService = function(sname){
      env.ui.GeneralAlert("You are trying to delete this service !",'Confirm Your Decision',function(){
      env.ui.ResponseDialog(admin.del_uri(sname),config,true,null);
      },false);
    }
    this.ResetService = function(sname){
      env.ui.GeneralAlert("You are trying to reset this service !",'Confirm Your Decision',function(){
      env.ui.ResponseDialog(admin.reset_uri(sname),config,true,null);
      },false);
    }
    this.EnableForum = function(sname){
      var request = env.ui.ResponseDialog(this.enable_forum_uri(sname),config,true
      ,null);
    }
    this.RegisterCallback = function(redirect_uri){
      var uri = this.register_uri;
      var update = null;
      function Register(form_obj){
        if(form_obj.confirm.value != form_obj.password.value){
          zoyoe.ui.ShowDialog(zoyoe.ui.dialog_title,false);
          zoyoe.ui.BuildErrorMsg("! Password not confirmed.")
          return;
        }
        var register_config = {
          method: 'GET',
          form: {id:form_obj}
        }
        if(redirect_uri){
          update = new function(){
            this.uri = redirect_uri;
          }
        }
        zoyoe.ui.GeneralDialogCont(uri,register_config,true,update);
      }
      return Register;
    }
 
    this.ShowRegisterDialog = function(){
      env.ui.InfoCollectDialog("Register",
      this.register_dialog_uri,"form-register",admin.RegisterCallback());
    }

    this.ChangePWDCallback = function(redirect_uri){
      var uri = this.change_pwd_uri;
      var update = null;
      function Register(form_obj){
        if(form_obj.confirm.value != form_obj.password.value){
          zoyoe.ui.ShowDialog(zoyoe.ui.dialog_title,false);
          zoyoe.ui.BuildErrorMsg("! Password not confirmed.")
          return;
        }
        var register_config = {
          method: 'GET',
          form: {id:form_obj}
        }
        if(redirect_uri){
          update = new function(){
            this.uri = redirect_uri;
          }
        }
        zoyoe.ui.GeneralDialogCont(uri,register_config,true,update);
      }
      return Register;
    }
 
    this.ShowChangePWDDialog = function(){
      env.ui.InfoCollectDialog("Change PWD",
      this.pwd_dialog_uri,"form-change-pwd",admin.ChangePWDCallback());
    }
    this.LoginCallback = function(cb){
      var uri = this.login_uri;
      function Login(form_obj){
        var login_config = {
          method: 'GET',
          form: {id:form_obj}
        }
        zoyoe.ui.GeneralDialogCont(uri,login_config,true);
      }
      return Login;
    }
    this.ShowLoginDialog= function(){
      env.ui.InfoCollectDialog("Login",
      this.login_dialog_uri,"form-login",admin.LoginCallback());
    }
    this.ShowAddServiceDialog = function(){
      env.ui.InfoCollectDialog("Restaurant",this.addserv_dialog_uri,"form-addservice",AddService);
    }
    this.AddReport = function(){
      var map_comp = zoyoe.map;/*Convention*/
      var script = document.createElement("script");
      zoyoe.ui.dialog_name = 'form-report';
      var form_obj = document.forms(zoyoe.ui.dialog_name);
      script.setAttribute("type","text/javascript"); 
      if (form_obj.address.value.length != 0){
        script.setAttribute("src",map_comp.SearchUri(form_obj.address.value+',NSW,Australia')
        +"&jsonp=AddReportJSON");    
        document.body.appendChild(script);
      }
      else{
        zoyoe.ui.GeneralAlert("You need give us a valid address for the restaurant","",null,false);
        zoyoe.ui.BuildErrorMsg('Please enter address !!');
      }
    }
    function Reload(){
      if(document.forms['reload']){
        document.forms['reload'].submit();
      }else{
        zoyoe.ALERT('Try alternative Reload Function');
        location.reload(true);
      }
    }
    this.Logout = function(){
      var logout_uri = "/core/user/logout/";
      YUI().use("io-form",function(Y){
        uri = logout_uri;
        var logout_config = {
          method: 'GET',
        }
        function complete(id,o,args){
          Reload();
        }
        Y.on('io:complete',complete);
        var request = Y.io(logout_uri,logout_config);
      });
    }
  }
  return admin;
}

function AddService(form_obj){
  zoyoe.ui.ShowDialog(zoyoe.ui.dialog_title,true);
  var map_comp = zoyoe.map;/*Convention*/
  var script = document.createElement("script");
  script.setAttribute("type","text/javascript"); 
  if (form_obj.address.value.length != 0){
    script.setAttribute("src",map_comp.SearchUri(form_obj.address.value+',NSW,Australia')
    +"&jsonp=AddServiceJSON");    
  }
  else{
    zoyoe.ui.BuildErrorMsg('Please enter address !!');
  }
  document.body.appendChild(script);
}
function BuildResultAddress(form_obj,result){
  if(result.resourceSets){
    if(result.resourceSets[0].estimatedTotal == 0){
      zoyoe.ui.BuildErrorMsg('Address Not Found !!');
      return null;
    }
    else if(result.resourceSets[0].estimatedTotal == 1){
      var resources = result.resourceSets[0].resources;
      if(resources[0].address.formattedAddress == "New South Wales"){
        zoyoe.ui.BuildErrorMsg("Address Not Found !!");
        return null;
      }else if(resources.length == 1){
        zoyoe.ALERT(resources[0].address.formattedAddress);
        form_obj.address.value = resources[0].address.formattedAddress; 
        var c = resources[0].point.coordinates;
        return c;
      }else{
        zoyoe.ui.BuildErrorMsg('Ambiguious Address,Please Make It Clear !!');
        return null;
      }
    }
    else{
      var resources = result.resourceSets[0].resources;
      zoyoe.ui.BuildErrorMsg('Multi Address Found,Please Make It Clear !!');
      return null;
    }
  }
}
function AddReportJSON(result){
  var form_obj = document.forms(zoyoe.ui.dialog_name);
  var c = BuildResultAddress(form_obj,result);
  if(c){
    var add_report_config = {
      method: 'POST',
      data:'latitude='+c[0]+"&longitude="+c[1],
      form: {id:form_obj}
    }
    var add_report_uri = "/core/data/addreport/";
    var request = zoyoe.ui.ResponseDialog(add_report_uri,add_report_config,true,null);
  }else{
    return;
  }
}
function AddServiceJSON(result){
  var form_obj = document.getElementById(zoyoe.ui.dialog_name);
  var days = new Array();
  var add_service_uri = "/core/data/addservice/";
  if(result.resourceSets){
    if(result.resourceSets[0].estimatedTotal == 0){
      zoyoe.ui.BuildErrorMsg('Address Not Found !!');
    }
    else if(result.resourceSets[0].estimatedTotal == 1){
      var resources = result.resourceSets[0].resources;
      if(resources[0].address.formattedAddress == "New South Wales"){
        zoyoe.ui.BuildErrorMsg("Address Not Found !!");
      }else if(resources.length == 1){
        zoyoe.ALERT(resources[0].address.formattedAddress);
        form_obj.address.value = resources[0].address.formattedAddress; 
        if(form_obj.Sun.checked){days.push("Sun");}
        if(form_obj.Mon.checked){days.push("Mon");}
        if(form_obj.Tue.checked){days.push("Tue");}
        if(form_obj.Wed.checked){days.push("Wed");}
        if(form_obj.Thu.checked){days.push("Thu");}
        if(form_obj.Fri.checked){days.push("Fri");}
        if(form_obj.Sat.checked){days.push("Sat");}
        var c = resources[0].point.coordinates;
        zoyoe.ALERT(days.join(','));
        var add_service_config = {
          method: 'POST',
          data:'latitude='+c[0]+"&longitude="+c[1]+"&days="+days.join(','),
          form: {id:form_obj}
        }
        zoyoe.ui.HideDialog();
        zoyoe.ui.GeneralDialogCont(add_service_uri,add_service_config,
          true,function(dom){
          var ss = dom.documentElement.getElementsByTagName('SERVICE');
          foreach(ss,function(ele){
            var service = new Service(ele);
            zoyoe.map.AddFocusService(service);
          });
        });
      }else{
        zoyoe.ui.BuildErrorMsg('Ambiguious Address,Please Make It Clear !!');
      }
    }
    else{
      var resources = result.resourceSets[0].resources;
      var select = "<form name='select-address'><select name='select' onchange=\"document.getElementById('address-input').value = this.options[this.selectedIndex].value\"><option value=''>---</option>";
      for(var i = 0; i < resources.length; i++){
        var option_val = resources[i].address.formattedAddress;
        select += "<option value='" + option_val + "' id='sel'>" + option_val + "</option>";
      }
      select += "</select></form>";
      zoyoe.ui.BuildErrorMsg('Multi Address Found,Please Make It Clear !!' + select);
    }
  }
}

function InitSearch(opt_ele_container,option_path){
  var search = new function(){
    this.option = option_path;
  };
  return search;
}
