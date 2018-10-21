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
%if state['exEn']:
   <td class="thead">E</td>
%end
   <td><a class="thead" href='{{state['qs']}}&sort=cat&order={{state['norder']}}'>Cat</a></td>
   <td><a class="thead" href='{{state['qs']}}&sort=subcat&order={{state['norder']}}'>SubCat</a></td>
   <td><a class="thead" href='{{state['qs']}}&sort=title&order={{state['norder']}}'>Titre</a></td>
   <td><a class="thead" href='{{state['qs']}}&sort=publish_date&order={{state['norder']}}'>Date</a></td>
   <td><a class="thead" href='{{state['qs']}}&sort=size&order={{state['norder']}}'>Taille</a></td>
   <td><a class="thead" href='{{state['qs']}}&sort=seed&order={{state['norder']}}'>Seed</a></td>
   <td><a class="thead" href='{{state['qs']}}&sort=leech&order={{state['norder']}}'>Leech</a></td>
   <td class="thead">Lien</td>
  </tr>
%for r in state['sorted_torrents']:
   <tr>
%if state['rtEn']:
    <td><a href="rt/{{r.tid}}">R</a></td>
%end
%if state['tsEn']:
    <td><a href="ts/{{r.tid}}">T</a></td>
%end
%if state['dgEn']:
    <td><a href="dg/{{r.tid}}">D</a></td>
%end
%if state['exEn']:
    <td><a href="ex/{{r.cat}}/{{r.subcat}}/{{r.tid}}">E</a></td>
%end
    <td>{{r.cat}}</td>
    <td>{{r.subcat}}</td>
%if state['ano']:
    <td><a class="torrent" href="{{r.get_dl_link()}}">{{r.title}}</a></td>
%else:
    <td><a class="torrent" href="dl/{{r.tid}}">{{r.title}}</a></td>
%end
    <td>{{r.publish_date}}</td>
    <td>{{r.nsize}}</td>
    <td>{{r.seed}}</td>
    <td>{{r.leech}}</td>
    <td><a href="{{r.href}}">X</a></td>
   </tr>
%end
 </table>
</div>
<div>
%if not state["qs"].startswith('top/'):
%if request.query.page:
<a href="{{state["qs"]}}&sort={{request.query.sort}}&order={{state['corder']}}&page={{str(int(request.query.page)-50)}}">&laquo;</a>
%end
%page = int(request.query.page) if request.query.page else 0
<a href="{{state["qs"]}}&sort={{request.query.sort}}&order={{state['corder']}}&page={{page+50}}">&raquo;</a>
%end
</div>

% include('footer.tpl')
