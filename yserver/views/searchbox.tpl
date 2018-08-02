% from bottle import request
  <div class="searchbox">
  <form method="GET" action="/search">
  Texte
  <input type='text' name='search' id='search' value='{{request.query.search}}'/>
  Cat
  <input type='text' name='cat' id='cat' value='{{request.query.cat}}'/>
  SubCat
  <input type='text' name='subcat' id='subcat' value='{{request.query.subcat}}'/>
  <input type='submit' value='Rechercher' id='search'/>
  </form>
  </div>
%end

