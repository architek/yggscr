<!DOCTYPE html>
<html>
 <head>
  <meta charset="UTF-8">
  <title>Ygg interface</title>
  <base href="{{request.script_name}}">
  <link rel="stylesheet"  type="text/css"     href="static/style.css">
  <link rel="icon"        type="image/gif"    href="images/pirate.gif">
  <script src="static/jquery.min.js"></script>
  <script src="static/xhr.js"></script>
  <script src="static/cat.js"></script>
 </head>
<body>
 <div class="menu" style="overflow:hidden;margin:0px;padding:0px">
  <div style="float:left;margin:0px;padding:0px;">
   <a href="reco"> <img border="0" alt="Reload" src="images/pirate.gif" width="30" height="20" style="border-radius: 50%;"/> </a>
  </div>
  <div class="menu" id="modal"> </div>
 </div>
 <div class="menu">
 <ul>
 <li><a class="menu" href="top/day">Torrents du jour</a></li>
 <li><a class="menu" href="top/week">Torrents de la semaine</a></li>
 <li><a class="menu" href="top/month">Torrents du mois</a></li>
 <li><a class="menu" href="top/exclus">Exclusivités</a></li>
 </ul>
 </div>

<script>
function tpl_disp_message() {
    %for msg in rtn:
        prog_fade("{{msg}}", 3000);
    %end
}
</script>

%if not state['ano']:
    % include('stats.tpl')
%end
% include('searchbox.tpl')
