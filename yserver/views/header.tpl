<!DOCTYPE html>
<html>
 <head>
  <meta charset="UTF-8">
  <title>Ygg interface</title>
  <link rel="stylesheet"  type="text/css"     href="/static/style.css">
  <link rel="icon"        type="image/png"    href="/images/transmission.png">
  <script type="text/javascript" src="/static/jquery.min.js"></script>
  <script type="text/javascript" src="/static/xhr.js"></script>
 </head>
<body>
 <div class="menu">
 <table style="padding:0px;margin:0px;border=0;">
 <tr>
 <td width="30%"> <div class="menu" id="modal" style="height:1em;padding:0px;margin:0px"></div> </td>
 <td>
 <ul>
 <li><a class="menu" href="/top/day">Torrents du jour</a></li>
 <li><a class="menu" href="/top/week">Torrents de la semaine</a></li>
 <li><a class="menu" href="/top/month">Torrents du mois</a></li>
 <li><a class="menu" href="/top/mostseeded">Torrents rapides</a></li>
 <li><a class="menu" href="/rss">Rss</a></li>
 </ul>
 </td>
 </tr>
 </table>
 </div>

<script>
function tpl_disp_message() {
    var idx = 0;
    %for msg in rtn:
        console.log("Fade message <"+"{{msg}}"+">");
        prog_fade("{{msg}}", idx);
        idx = idx +1;
    %end
}
</script>

% include('stats.tpl')
% include('searchbox.tpl')
