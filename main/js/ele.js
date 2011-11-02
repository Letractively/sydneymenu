if(zoyoe){
  zoyoe.ElementExtension = new function(){
    this.auto_container = null;
    this.selectedIndex = -1;
    this.inputValue = "";
    this.BuildExtensionElements = function(root){
      YUI().use('node',function(Y){
        if(!root){root = Y.one("body");}
        var photo_list_exts = root.all('div.extension-photo-player'); 
        photo_list_exts.each(function(container){
          var input = container.one('input');
          var iframe_container = Y.Node.create("<div></div>");
          var iframe = Y.Node.create("<iframe></iframe>");
          iframe_container.append(iframe);
          iframe.setStyle("display","none");
          iframe.on('load',function(){
            iframe.setStyle("display","block");
            iframe.setStyle("width","100%");
            iframe.setStyle("height","100%");
          }); 
          iframe.set("src",'/core/gallery/'+zoyoe.service_name+"/play/" + input.get("value") + "/");
          container.append(iframe_container);
        });

/* Build Drop List 

 */
      	var drop_list_exts = root.all('div.extension-drop-list');
      	drop_list_exts.each(function(container){
          var input = container.one('input');
          var current = container.one('div.current');
          var current_value = (input.get('value'));
          current.set('innerHTML',current_value);
          var options = container.all('li');
          container.all('span').set('innerHTML',"&#9744");
          for(var i=0;i<options.size();i++){
            if(options.item(i).one("h5").get("innerHTML") == current_value){
              options.item(i).one('span').set('innerHTML',"&#9746");
            }
          }
          options.on('click',function(e){
            var curele = e.currentTarget;
            container.all('span').set('innerHTML',"&#9744");
            curele.one('span').set('innerHTML',"&#9746");
            var hint = curele.one('h5').get('innerHTML');
            Y.Node.getDOMNode(input).value = hint;
            container.one('div.current').set('innerHTML',hint);
          });
          /* There we do not provide any way to handle customer event while select event was triggered.
          You need to handle the input event to trigger customer handler.
          */
        });
      	var dict_select_exts = root.all('div.extension-dict-select');
      	dict_select_exts.each(function(container){
          var input = container.one('input');
          var options = container.all('li.item');
          options.on('click',function(e){
            var curele = e.currentTarget;
            var item_value = curele.one('h5').get('innerHTML');
            var key_value = curele.get("parentNode").get("parentNode").one("span.key").get("innerHTML");
            var hint = key_value + "/" + item_value;
            var dom_input = Y.Node.getDOMNode(input);
            dom_input.value = hint;
            container.one('div.current').set('innerHTML',hint);
            if(dom_input.ext_onchange){
               dom_input.ext_onchange(hint);
            }
          });
          /* There we do not provide any way to handle customer event while select event was triggered.
          You need to handle the input event to trigger customer handler.
          */
        });
 
        var combo_select_exts = root.all('div.extension-combo-select');
        combo_select_exts.each(function(container){
          var input = container.one('input');
          var inputNode = Y.Node.getDOMNode(input);
          var options = container.all('li');
          var items = inputNode.value.split(",");
          var options = container.all('li');
          container.all('span').set('innerHTML',"&#9744");
          for (var i=0;i<items.length;i++){
            for(var j=0;j<options.size();j++){
              if(options.item(j).one("h5").get("innerHTML") == items[i]){
                options.item(j).one('span').set('innerHTML',"&#9746");
              }
            }
          }
          if(inputNode.value == 0) {
            container.one('div.current').set('innerHTML', "NIL");
          }else{
            if(inputNode.value.indexOf(",") != -1) {
              container.one('div.current').set('innerHTML',"Multiple");
            }else{
              container.one('div.current').set('innerHTML',inputNode.value);
            }
          }
          options.on('click', function(e){
            var curEle = e.currentTarget;
            var curEleSpan = curEle.one('span');
            if(escape(curEleSpan.get('innerHTML')) === "%u2612") {
              curEleSpan.set('innerHTML', "&#9744");
            } else if(escape(curEleSpan.get('innerHTML')) === "%u2610"){
              curEleSpan.set('innerHTML', "&#9746");
            }
            var hint = curEle.one('h5').get('innerHTML');
            if(inputNode.value.indexOf(hint) != -1) {
              if(inputNode.value.indexOf("," + hint) != -1) {
                hint = inputNode.value.replace("," + hint, "");
              } else if(inputNode.value.indexOf(hint + ",") != -1) {
                hint = inputNode.value.replace(hint + ",", "");
              } else {
                hint = inputNode.value.replace(hint, "");
              }    
            } else {
              if(inputNode.value.length != 0) {
                hint = inputNode.value.concat("," + hint);
              }
            }
            inputNode.value = hint;
            if(hint.length == 0) {
              container.one('div.current').set('innerHTML', "NIL");
            } else {
              if(inputNode.value.indexOf(",") != -1) {
                container.one('div.current').set('innerHTML',"Multiple");
              }else{
                container.one('div.current').set('innerHTML',hint);
              }
            }
          });
        });

/* 
    ZOYOE Extension AutoComplete
    lable = "div.extension-auto-complete"
 */
        var auto_complete_exts = root.all('div.extension-auto-complete');
        auto_complete_exts.each(function(container){
          var input = container.one("input");
          var hint = container.one("div.autocomp-drop-list ul");
          zoyoe.ElementExtension.auto_input = input;
          zoyoe.ElementExtension.auto_container = container;
          input.on('keyup', function(e){
            var dropList = container.one("div.autocomp-drop-list ul");
            if (e.keyCode == 38 || e.keyCode == 40) {
              var listSize = dropList.all('li').size();
              if(listSize == 0) {
                return;
              }
              var selectedIndex = zoyoe.ElementExtension.selectedIndex;
              var previousIndex = selectedIndex;
              if(e.keyCode == 38) {
                selectedIndex -= 1;
                if(selectedIndex < 0) {
                  selectedIndex = listSize - 1;
                }
              } else {
                selectedIndex += 1;
                if(selectedIndex == listSize) {
                  selectedIndex = 0;
                }
              }
              var previousSelectedNode = dropList.all('li').item(previousIndex);
              var selectedNode = dropList.all('li').item(selectedIndex);
              if(previousIndex >= 0) {
                previousSelectedNode.setStyle('background', '');
              }
              selectedNode.setStyle('background', '#eee');
              var getText = selectedNode.one('h5').get('innerHTML');
              input.set('value', getText);
              zoyoe.ElementExtension.selectedIndex = selectedIndex;
              zoyoe.ElementExtension.inputValue = getText;
              return;
            } else if(e.keyCode == 13) {
              PreSearch();
              return;
            }
            if(input.get("value") == zoyoe.ElementExtension.inputValue) {
              return;
            } else {
              zoyoe.ElementExtension.inputValue = input.get("value");
            }
            if(input.get("value").length == 0) {
              if(hint.get('innerHTML').length != 0)
                hint.set('innerHTML', "");
            } else {
              var dom_input = Y.Node.getDOMNode(input);
              if(dom_input.ext_onchange){
                dom_input.ext_onchange(input.get("value"));
              }
            }
          });
        });
/* Finish YUI.use */
      });
    }
  }
}
function ExtensionTest(){
  if(zoyoe&&zoyoe.ElementExtension){
    zoyoe.debug = true;
    zoyoe.map = new MapInfoCore(function(){},null,null,null);
    zoyoe.ElementExtension.BuildExtensionElements();
    YUI().use("node",function(Y){
       var input = Y.one("div.extension-auto-complete").one("input");
       var dom_input = Y.Node.getDOMNode(input);
       dom_input.ext_onchange = function(searchStr){
         if(zoyoe.map){
            zoyoe.map.TargetPlace(searchStr,"AutoCompJSON");
         } else {
         zoyoe.ALERT("Map not loaded");
         }
       }
    });
  }
}

function AutoCompJSON(result){
  var container = zoyoe.ElementExtension.auto_container;
  var hint = container.one("div.autocomp-drop-list ul");
  hint.set("innerHTML","");
  if(result.resourceSets){
    var resources = result.resourceSets[0].resources;
    if(resources.length == 0){
    }else{
      for(i = 0; i < resources.length; i ++){
        var addr = resources[i].address.formattedAddress;
        var li_html = "<li><h5>";
        li_html += addr;
        li_html += "</h5></li>";
        YUI().use("node",function(N){
          var li = N.Node.create(li_html);
          hint.append(li);
          li.on('click',function(e){
            var addr = N.Node.getDOMNode(e.currentTarget).firstChild.innerHTML;
            container.one("input").set("value",addr);
          });
        });
      }
    }
  }
}
