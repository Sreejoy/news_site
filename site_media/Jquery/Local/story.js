var item_per_page=5; //no of items to be displayed per page, can be changed from a dropdown
var item_page_current=1; // current page no.
var user = $.session.get('user'); // retrieve user from session
var token = localStorage.getItem('token'); //retrieve token from session
var search_result=[]; //search result
var clicked_news_id=""; //post id of the post that was clicked, needed for update
var create_or_update=""; //in create mode or update mode


$(document).ready(function(){
    if (typeof token === 'undefined' || token == ''){ //if user is already logged in redirect to all story page
        window.location.href = '/';
    }

    all_functions();

    $(".page-content").css({'display' : 'inline-block'});
});


//has all the functions
function all_functions()
{
    delete_or_create_or_update();
    logout();
    search();
    get_news(item_per_page,item_page_current);
    DeleteSearchQueryText(item_per_page,item_page_current);
    per_page_item_settings();
}

//handles how many items will be displayed
function per_page_item_settings()
{
    item_per_page = $("#perpageitem").val();
    $('#perpageitem').on('change',function(){
        if($(this).val()!=''){
            item_per_page=$(this).val();
            item_page_current=1;
            $('#pagination_div').pagination('destroy');
            window.location.hash = "#1";
            get_news(item_per_page,item_page_current);
        }
    });
}

//handles search suggestion
function search()
{
    $("#searchbox").select2({
        placeholder: "Search News....",
        width: 460,
        quietMillis: 250,
        ajax: {
            url: "search_suggestions",
            dataType: "json",
            queitMillis: 250,
            data: function(term, page) {
                return {
                    'term': term,
                    'page': page
                };
            },
            results: function(data, page) {
                return {
                    results: data.items,
                    more: data.more
                }
            }
        },
        formatResult: format_bug_search,
    }).on("change", function(e) {
        var value_id=$(this).select2('data')['id'];
        var tag_id=$(this).select2('data')['type'];
        if(tag_id=='Suggestions'){
            var message='You can search by keywords "@'+value_id+"\"";
            alertify.success(message);
            var place = '@'+value_id+'=';
            $(this).select2('val', '');
            $(this).select2("open");
            $(".select2-input").val(place);
            return false;
        }
        if(tag_id!='Bug'){
            var value_to_show=$(this).select2('data')['text'].split("").reverse().join("").split(" - ")[1].split("").reverse().join("").trim();
        }else{
            var value_to_show=value_id;
        }


        $("#AutoSearchResult #searchedtext").html('<td><img class="delete" title = "Delete" src="/static/delete4.png" style="width: 30px; height: 30px"/></td>'
                + '<td class="Text" data-id="'+value_id+'">'
                + value_to_show + ' - '+tag_id
                + ": "
                + '</td>');

        $(this).select2('val','');
        get_news(item_per_page,item_page_current);
        return false;
    });
}

//logs out user and value of user and token variable in session set to empty string
function logout(){
        $('#logout').live('click',function () {

              $.get("/logout",{'username':user,'token':token},function(data)
              {
                  $.session.set('user', '');
                  $.session.set('token', '');
                  localStorage.setItem("user", '');
                  localStorage.setItem("token", '');
                  window.location.href = '/';
              });

         });
        return false;
}

//shows delete view and handles delete
function handle_delete(){
    $('.delete_news').live('click',function () {
        var this_text = $(this).attr('id');
        var news_id = this_text.substring(this_text.indexOf("_")+1);
        console.log(news_id);
        bootbox.confirm("Are you sure to delete this news ?", function(result) {
               if(result){

                    $.get("delete_story",{'news_id' : news_id,'token':token},function(data)
                        {
                            if(data['code'] === '1'){
                                alertify.success("News Deleted Successfully");
                                get_news(item_per_page,item_page_current);
                            }
                            else{
                                alertify.error("Couldn't delete news. Please  try again later.");
                            }

                        });


               }
            });
          return false;
    });
}

//shows update view
function handle_update(){
    $('.update_news').live('click',function () {
        console.log("in update news");
        var this_text = $(this).attr('id');
        var news_id = this_text.substring(this_text.indexOf("_")+1);
        clicked_news_id = news_id;
        create_or_update = 'update';
        for(var i=0;i<search_result.length;i++){
            if(search_result[i][0] == clicked_news_id){
                console.log(search_result[i]);
                $("#title").val(search_result[i][1]);
                $("#body").val(search_result[i][2]);
                $("#author").val(search_result[i][3]);
            }
        }
        return false;
    });
}

//shows create view
function handle_create(){
    $('#create_news').live('click',function () {
        console.log("in create news");
        clicked_news_id = '';
        create_or_update = 'create';
        return false;
    });
}

//shows submit(create/update) of news
function handle_submit(){
    $('#submit_news').live('click',function () {
        var title = $("#title").val();
        var body = $("#body").val();
        var author = $("#author").val();
        if(title === ""||body === ""||author === ""){
            alertify.error("Fields can't be empty");
            return;
        }
        $("#title").val("");
        $("#body").val("");
        $("#author").val("");
        if(create_or_update === "update"){ //update
            $.ajax({
                url: "update_story/",
                data: {
                    "news_id": clicked_news_id,
                    "title": title,
                    "body": body,
                    "author": author,
                    "token": token
                },
                type: "POST",
                dataType: "json",
                success: function(data) {
                    if (data['code'] === '0') {
                        alertify.error(data['message']);
                    } else if (data['code'] === "1") {
                        alertify.success(data['message']);
                        get_news(item_per_page,item_page_current);
                    } else {
                        alertify.error("Something went wrong! Please check server settings.");
                    }
                }
            });
        }
        else{ //create
            $.ajax({
                url: "create_story/",
                data: {
                    "title": title,
                    "body": body,
                    "author": author,
                    "token": token
                },
                type: "POST",
                dataType: "json",
                success: function(data) {
                    if (data['code'] === '0') {
                        alertify.error(data['message']);
                    } else if (data['code'] === "1") {
                        alertify.success(data['message']);
                        get_news(item_per_page,item_page_current);
                    } else {
                        alertify.error("Something went wrong! Please check server settings.");
                    }
                }
            });
        }
        return false;
    });

}

function delete_or_create_or_update() {
    handle_delete();
    handle_update();
    handle_create();
    handle_submit()
}

//searches news
function get_news(item_per_page,item_page_current){

    var search_text='';
    $("#AutoSearchResult #searchedtext td.Text").each(function() {
        search_text=$(this).attr('data-id');
    });

    //calls search api
    $.get("read_story",{
        'search_text':search_text,
        'method':'json' ,
        'token':token,
        'item_per_page':item_per_page,
        'item_page_current':item_page_current
    },function(data){
        if(data['TableData'].length>0){
            search_result = data['TableData'];
            form_table("AllMSTable",data['Heading'],data['TableData'],data['count'],"News");
            $('#pagination_div').pagination({
                items:data['count'],
                itemsOnPage:item_per_page,
                cssStyle: 'dark-theme',
                currentPage:item_page_current,
                displayedPages:2,
                edges:2,
                hrefTextPrefix:'#',
                onPageClick:function(PageNumber){
                    get_news(item_per_page,PageNumber);
                }
            });
        }else{
            console.log("No data found");
            $("#AllMSTable").empty();
            $("#AllMSTable").html('<b>No News Found</b>');
            $("#pagination_div").pagination('destroy');
        }
    });

}

//forms news feed table
function form_table(divname,column,data,total_data,type_case){
    var tooltip=type_case||':)';
    var message='';
    message+= "<p class='Text hint--right hint--bounce hint--rounded' data-hint='" + tooltip + "' style='color:#0000ff; font-size:12px;'>" + total_data + " " + type_case+"</p>";
    message+='<table>';
    message+='<thead><tr>';

    message+='</tr></thead><tbody>';
    for(var i=0;i<data.length;i++){
        message+='<tr>';

        message+='<td><br><font size="3" color="#FF1493"><b>'+data[i][1]+'</b></font><br><br><font color="#483D8B" size="2">'+data[i][2]+'</font><br><br> <font color="#FF1493"> <b>By '+data[i][3]+'</b></font>' +
                                  '<br><br><button id="update_' +data[i][0] + '"  data-target="#modal_create" data-toggle="modal" class="btn blue btn-outline sbold uppercase update_news" type="button"><i class="fa fa-edit"></i> Update</button>'+
                                   '&nbsp;&nbsp;<button id="delete_' +data[i][0] + '" class="btn red btn-outline  sbold uppercase delete_news" type="button"><i class="fa fa-remove"></i> Delete</button><hr></td>';

        message+='</tr>';
    }
    message+='</tbody></table>';
    $('#'+divname).html(message);

}

//markup needed for search suggestion
function format_bug_search(req) {
    var markup ='<div><i class="fa fa-file"></i><span style="font-weight: bold;"><span> ' + req.text + '</span></div>';
    return markup;
}


//if user deletes a search
function DeleteSearchQueryText(item_per_page,item_page_current){
    $("#AutoSearchResult td .delete").live('click', function() {
        $('#pagination_div').pagination('destroy');
        $('#AllMSTable').empty();
        //check it is second from last

        $(this).parent().next().remove();
        $(this).parent().remove();


        get_news(item_per_page,item_page_current);
    });
}

