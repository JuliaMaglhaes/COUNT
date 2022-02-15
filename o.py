def number_of_locations(self):
        count_array = []
        count=0
        for a in Area.objects.all():
            for obj in Location.objects.all():
                #print (str(obj.area.id)+" vs "+str(a.id))
                if obj.area.id == a.id:
                    print("check")
                    count+=1
            count_array.append(count)
            count=0
        return count_array