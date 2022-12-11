def show_venue(request, venue_id):
    object = get_object_or_404(Venue, pk=venue_id)
    context={}
    print(object)
    
    #hit count logic
    hit_count=get_hitcount_model().objects.get_for_object(object)
    print(hit_count)
    hits = hit_count.hits
    print(hits)
    
    hitcontext = hitcount = {'pk':hit_count.pk}
    print(hitcount)
    
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    print(hit_count_response)
    
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits
        print()
        
       
    if request.method == "POST" and 'btnreview_form' in request.POST:
        form = CatalogueReviewForm(request.POST)
        data = form.save(commit=False)
        data.product_id = venue_id
        data.catalogue_id = venue_id

        data.user_id = request.user.id
        data.save()
        ven_id = request.POST.get('venue_id')
        if form.is_valid():
            print(data)
            form.save()
            return HttpResponseRedirect(ven_id)
    else:
        venue = Venue.objects.get(pk=venue_id)
        menu = Catalogue.objects.filter(venue=venue_id)
        categories = Catalogue.objects.filter(venue=venue_id).order_by('category_order')

    return render(request, 'main/show_venue.html',{'venue':venue, 'menu':menu, 'categories':categories,'product':product,'venue_id':venue_id,'object':object,'hitcount':hitcount})
