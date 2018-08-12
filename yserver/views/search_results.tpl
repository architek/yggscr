% include('header.tpl')
<div class="results">
<table>
  <tr>
% from bottle import request
%if state['rtEn']:
   <td class="thead">R</td>
%end
%if state['tsEn']:
   <td class="thead">T</td>
%end
%if state['dgEn']:
   <td class="thead">D</td>
%end
   <td class="thead">Cat</td>
   <td class="thead">SubCat</td>
   <td><a class="thead" href='{{state['qs']}}&sort=name&revorder=1'>Titre</a></td>
   <td><a class="thead" href='{{state['qs']}}&sort=publish_date&revorder=1'>Date</a></td>
   <td><a class="thead" href='{{state['qs']}}&sort=size&revorder=1'>Taille</a></td>
   <td><a class="thead" href='{{state['qs']}}&sort=seed&revorder=1'>Seed</a></td>
   <td><a class="thead" href='{{state['qs']}}&sort=leech&revorder=1'>Leech</a></td>
   <td class="thead">Lien</td>
  </tr>
%for r in state['sorted_torrents']:
   <tr>
%if state['rtEn']:
    <td><a href=/rt/{{r.tid}}>R</a></td>
%end
%if state['tsEn']:
    <td><a href=/ts/{{r.tid}}>T</a></td>
%end
%if state['dgEn']:
    <td><a href=/dg/{{r.tid}}>D</a></td>
%end
    <td>{{r.cat}}</td>
    <td>{{r.subcat}}</td>
    <td><a class="torrent" href=/dl/{{r.tid}}>{{r.title}}</a></td>
    <td>{{r.publish_date}}</td>
    <td>{{r.size}}</td>
    <td>{{r.seed}}</td>
    <td>{{r.leech}}</td>
    <td><a href='{{r.href}}'>X</a></td>
   </tr>
%end
 </table>
</div>
<div>
%if request.query.page:
<a href='{{state["qs"]}}&sort={{request.query.sort}}&page={{str(int(request.query.page)-50)}}'>&laquo;</a>
%end
%page = int(request.query.page) if request.query.page else 0
<a href='{{state["qs"]}}&sort={{request.query.sort}}&page={{page+50}}'>&raquo;</a>
%end
</div>

% include('footer.tpl')
