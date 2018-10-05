/*
for c in yggscr.link.list_cats():
     a=','.join('"' + e + '"' for e in yggscr.link.list_subcats(c))
     print('cat["'+c+'"]=['+a+'];')
*/
var cat = new Object();
cat[""]=[""];
cat["filmvidéo"]=["animation","animation-serie","concert","documentaire","emission","film","serie","spectacle","sport","video"];
cat["audio"]=["karaoke","musique","podcast","samples"];
cat["application"]=["autre","formation","linux","macos","smartphone","tablette","windows"];
cat["jeu+vidéo"]=["autre","linux","macos","microsoft","nintendo","smartphone","sony","tablette","windows"];
cat["ebook"]=["audio","bds","comics","livres","mangas","presse"];
cat["emulation"]=["emulateurs","roms"];
cat["gps"]=["applications","cartes","divers"];
cat["xxx"]=["films","hentai","images"];

function subcat_select() {
    $('#cat').change(function() {
        var sel = $( this ).val();
        $('#subcat').empty();
        $.each( cat[sel], function( key, value ) {
            $('#subcat').append('<option value="'+value+'">'+value+'</option>');
        });
        $('#subcat').val($SUBCAT);
    });
    $.each( cat[""], function( key, value ) {
        $('#subcat').append('<option value="'+value+'">'+value+'</option>');
    });
    $.each( cat, function( key, value ) {
        $('#cat').append('<option value="'+key+'">'+key+'</option>')
    });
    $('#cat').val($CAT).change();
}

