% include('header.tpl')
<div>
<br />
<div class="results">
<table>
    <tr> <th> Choose RSS category </th> </tr>
%for t in results:
   <tr>
    <td><a class="torrent" href="/rss/{{!t}}">{{!t}}</a></td>
   </tr>
%end
 </table>
 </div>
</div>
% include('footer.tpl')
