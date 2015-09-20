/**
 * Created by ric on 2015-09-20.
 */

var az_search_key = "111E82222FF409389A920A64F6E7911E"

function search_enter_handle(e){
    if(e.keyCode === 13){
        exec_search($('#search_box').val());
    }
    return false;
}

function open_img_handle(){
    resp=JSON.parse(this.responseText);
    console.log(resp);
    window.location.href = resp['url'];
}

function open_img (search_id){
    var oReq = new XMLHttpRequest();
    oReq.addEventListener("load", open_img_handle);
    console.log("QERY IS "+search_id);
    var url = "https://voyagr.search.windows.net/indexes/photos/docs/"+search_id+"?api-version=2015-02-28"
    oReq.open("GET", url);
    //oReq.setRequestHeader("Content-Type", "application/json; charset=utf-8");
    oReq.setRequestHeader("api-key", az_search_key);
    oReq.send();
}

function suggestion_listener () {
    resp=JSON.parse(this.responseText);
    console.log(resp);
    var search_result = document.getElementById("search_result");
    search_result.innerHTML="\<ul id=\"search_result_li\" class=\"list-group\"\></ul>";
    var ul = document.getElementById("search_result_li");
    ul.innerHTML = '';

    for(i in resp['value']){
        sugg_tag = resp['value'][i]['@search.text'];
        var li = document.createElement("li");
        li.appendChild(document.createTextNode(sugg_tag));
        li.className = 'list-group-item';
        li.setAttribute('onclick','exec_search(\''+sugg_tag+'\')');
        ul.appendChild(li)
    }
}

function search_listener () {
    resp = JSON.parse(this.responseText);
    console.log(resp);

    var search_result = document.getElementById("search_result");
    search_result.innerHTML = "\<ul id=\"search_result_li\" class=\"list-group\"\></ul>";
    var ul = document.getElementById("search_result_li");
    ul.innerHTML = '';

    for (i in resp['value']) {
        sugg_tag = resp['value'][i]['@search.text'];
        var li = document.createElement("li");
        //li.appendChild(document.createTextNode("\<img src=\"" + thumb_url + ">\</img>" + sugg_tag));
        li.appendChild(document.createTextNode(resp['value'][i]['url']));
        li.className = 'list-group-item';
        li.setAttribute('onclick', 'open_img(\'' + resp['value'][i]['search_id'] + '\')');
        ul.appendChild(li)
    }
}

function exec_suggestion(query){
    var oReq = new XMLHttpRequest();
    oReq.addEventListener("load", suggestion_listener);
    console.log("QERY IS "+query);
    //var url = "https://voyagr.search.windows.net/indexes/photos/docs/suggest?api-version=2015-02-28&search="+query+"&$filter=user_id eq \'"+"aa"+"\'&suggesterName=image_tags"
    var url = "https://voyagr.search.windows.net/indexes/photos/docs/suggest?api-version=2015-02-28&search="+query+"&suggesterName=image_tags"
    oReq.open("GET", url);
    oReq.setRequestHeader("Content-Type", "application/json; charset=utf-8");
    oReq.setRequestHeader("api-key", az_search_key);
    oReq.send();
}

function exec_search(query){
    var oReq = new XMLHttpRequest();
    oReq.addEventListener("load", search_listener);
    console.log("QERY IS "+query);
    var url = "https://voyagr.search.windows.net/indexes/photos/docs?api-version=2015-02-28&search="+query
    oReq.open("GET", url);
    oReq.setRequestHeader("Content-Type", "application/json; charset=utf-8");
    oReq.setRequestHeader("api-key", az_search_key);
    oReq.send();
}


