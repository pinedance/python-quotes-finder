let ref_text = document.getElementById("ref-raw").innerText.trim()
let trg_text = document.getElementById("trg-raw").innerText.trim()

// console.log(ref_text)
// let ref_text = document.getElementById("ref-raw").textContent
// let trg_text = document.getElementById("trg-raw").textContent

let ref_text_tag = document.getElementById("ref-text")
let trg_text_tag = document.getElementById("trg-text")
let ref_text_len = ref_text.length
let trg_text_len = trg_text.length

let indices_len = trg_indices.length

let ref_traced, trg_traced
[ref_traced, trg_traced] = traceText( trg_indices, ref_text_len, trg_text_len )

let ref_text_seg = mergeTraceText(ref_traced)
let trg_text_seg = mergeTraceText(trg_traced)

const PREFIX = {
    ref: "Ref",
    trg: "Trg"
}

const CLASSNAME = {
    pair: "pair",
    highlight: "highlight",
    focus: 'focus'
}

function traceText( indices, ref_text_len, trg_text_len ){

    // let ref_space_count = new Array( ref_text_len+1 ).fill(0);
    let ref_space_idx = new Array( ref_text_len+1 ) //.fill( new Array() );
    // let trg_space_count = new Array( trg_text_len+1 ).fill(0);
    let trg_space_idx = new Array( trg_text_len+1 ) //.fill( new Array() );

    indices.forEach( function(e, i, arr){
          let ref_start, ref_stop, trg_start, trg_stop
          [[ref_start, ref_stop], [trg_start, trg_stop]] = e

          for (let j=ref_start; j<ref_stop; j++){
              // ref_space_count[j] += 1
              if ( ref_space_idx[j] ){
                  ref_space_idx[j].push( i )
              } else {
                  ref_space_idx[j] = [i]
              }
          }

          for (let k=trg_start; k<trg_stop; k++){
              // trg_space_count[k] += 1
              if ( trg_space_idx[k] ){
                  trg_space_idx[k].push( i )
              } else {
                  trg_space_idx[k] = [i]
              }
          }
    })

    return [ref_space_idx, trg_space_idx]
}

function mergeTraceText( traced ){
    let last_var, current_var // = traced[0]
    let start = 0
    let rst = []

    for( let i=0; i<traced.length; i++){
        last_var = traced[i-1] || []
        current_var = traced[i] || []
        if (  ( JSON.stringify( current_var ) == JSON.stringify( last_var ) ) ){
            // continue;
        } else {
            // console.log( i )
            // console.log( [ last_var, current_var ] )
            // console.log( [ [start, i], last_var ] )
            rst.push( [ [start, i], last_var ] )
            start = i
        }
    }

    rst.push( [ [start, traced.length], traced[traced.length-1] || [] ] )
    return rst
}

function createSpanFunc( type, whole_text, indices_len ){
    return function( e, i, arr ){
        let start, stop, idx_arr
        [[start, stop], idx_arr] = e
        let span = document.createElement("span");

        span.classList.add( CLASSNAME.pair )
        span.classList.add( type )
        let brightness = idx_arr.length
        span.classList.add( CLASSNAME.highlight )
        span.classList.add( CLASSNAME.highlight + "-" + String( ( brightness < 9 )? brightness : 9 ) )

        let span_text = whole_text.slice( start, stop )
        let span_text_by_line = span_text.split(/\r?\n/)

        for (let j=0; j<span_text_by_line.length; j++){
            let text_node = document.createTextNode( span_text_by_line[j] )
            span.appendChild( text_node )
            if( j != ( span_text_by_line.length - 1 ) ){
                span.appendChild( document.createElement("br") )
            }
        }

        if(idx_arr.length > 0){
            for ( let k=0; k<idx_arr.length; k++) {
                span.classList.add( type + "-" + String(idx_arr[k]+1) )
                addShoulderNum( span, type, idx_arr[k] );
            }
        }

        return span
    }
}

function addShoulderNum( parents_tag, type, j ){

    let sup = document.createElement("sup");
    sup.style = "cursor:pointer;"
    sup.onclick = linkFunc(j)
    let text_node = document.createTextNode("[" + String(j+1) + "]")
    sup.appendChild( text_node )
    parents_tag.appendChild( sup )
}

function createButton(context, func, label) {
    var button = document.createElement("input");
    button.type = "button";
    button.value = label;
    button.onclick = func;
    context.appendChild(button);
}

function refreshContents(){
      // console.log( ref_text_seg )
      // console.log( trg_text_seg )

      remove_highlight_pair()

      let ref_text_span = ref_text_seg.map( createSpanFunc( PREFIX.ref, ref_text, indices_len ) )
      let trg_text_span = trg_text_seg.map( createSpanFunc( PREFIX.trg, trg_text, indices_len ) )

      ref_text_span.forEach(function(e,i,arr){
          ref_text_tag.appendChild( e )
      })

      trg_text_span.forEach(function(e,i,arr){
          trg_text_tag.appendChild( e )
      })
      document.getElementById('ref-text').scrollIntoView();
      document.getElementById('trg-text').scrollIntoView();
}

function remove_highlight_pair(  ){
    let all_pair = document.getElementsByClassName( CLASSNAME.pair )
    for (let i=0; i<all_pair.length; i++){
        all_pair[i].classList.remove( CLASSNAME.focus )
    }
}

function highlight_pair( idx ){

    let ref_item = document.getElementsByClassName( PREFIX.ref + '-' + String(idx+1) )
    let trg_item = document.getElementsByClassName( PREFIX.trg + '-' + String(idx+1) )

    for (let j=0; j<ref_item.length; j++){
        ref_item[j].classList.add( CLASSNAME.focus )
    }

    for (let k=0; k<trg_item.length; k++){
        trg_item[k].classList.add( CLASSNAME.focus )
    }
}

function linkFunc( idx ){
    return function(){

      let ref_item = document.getElementsByClassName( PREFIX.ref + '-' + String(idx+1) )
      let trg_item = document.getElementsByClassName( PREFIX.trg + '-' + String(idx+1) )

      highlight_pair( idx )
      ref_item[0].scrollIntoView();
      // document.getElementById('ref-text').scrollBy(0, -100);
      trg_item[0].scrollIntoView();
      // document.getElementById('trg-text').scrollBy(0, -100);
      console.log( "Button: Pair" + String(idx+1) + " ； " + "IDX: " + String(idx) )
    }
}

window.onload = function() {

    refreshContents()
//
    let common_btn = document.getElementById("common-btn")
    let ref_btn = document.getElementById("ref-btn")
    let trg_btn = document.getElementById("trg-btn")
    createButton( common_btn, refreshContents, "refresh" )
    trg_indices.forEach(function (item, index, array) {
        createButton( trg_btn, linkFunc(index), "Pair"+String(index+1) )
    });

};
