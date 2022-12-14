
from accounts.models import CarerProfile, HomeProfile
from rest_framework import generics, permissions, views, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializer import AVSerializer, AssignedSerializer, ShiftSerializer
from .models import AssignedCarer, Availability, Shift



@api_view(["GET"])
def get_shifts(request, *args, **kwargs):
    user = request.user
    if user:
        if user.is_admin:
            shift_qs = Shift.objects.all()
            serializer = ShiftSerializer(shift_qs, many=True)
            return Response(serializer.data, status = 200)
        elif user.is_home:
            shift_qs = Shift.objects.filter(home__user=user)
            serializer = ShiftSerializer(shift_qs, many=True)
            return Response(serializer.data, status = 200)
    return Response({"message":"Error"}, status = 400)



@api_view(["POST"])
def publish_shifts(request, *args, **kwargs):
    user = request.user
    shift = request.data
    home = HomeProfile.objects.filter(id=shift['HOME_ID']).first()
    shift_qs = Shift.objects.create(home=home, day=shift["DAY"], month=shift["MONTH"],longday=shift["LONGDAY"],night=shift["NIGHT"], late=shift["LATE"], early=shift["EARLY"], year=shift["YEAR"])
    ser = ShiftSerializer(shift_qs)
    return Response(ser.data, status = 200)

@api_view(["POST"])
def assign_shifts(request, *args, **kwargs):
    data = request.data
    shift_id = data["shift_id"]
    assigned = data['assigned']
    ass_qs = [AssignedCarer(shift=Shift.objects.get(id=shift_id), type=shift["type"], carer=CarerProfile.objects.get(id=shift["carer_id"])) for shift in assigned]
    ass = AssignedCarer.objects.bulk_create(ass_qs)
    return Response(AssignedSerializer(ass, many=True).data, status=201)

@api_view(["POST"])
def complete_shift(request, *args, **kwargs):
    data = request.data
    shift = Shift.objects.filter(id=data['shift_id']).first()
    carer = CarerProfile.objects.filter(id = data["carer_id"]).first()
    assigned = shift.assigned.all()
    if carer in assigned:
        shift.covered.add(carer)
        return Response(ShiftSerializer(shift).data, status=201)
    else:
        return Response({"message":"Error"}, status=400)



@api_view(["GET"])
def get_avail(req, *args, **kwargs):
    user = req.user
    if user.carer:
        av = Availability.objects.filter(carer__user = user).first()
        if av:
            return Response(AVSerializer(av).data, status=200)
        else:
            new_av =  Availability.objects.create(carer = CarerProfile.objects.filter(user = user).first())
            return Response(AVSerializer(new_av).data, status=200)
    else:
        return Response({}, status=403)

@api_view(["POST"])
def post_avail(req, *args, **kwargs):
    print(req.data, "daatttataa")
    user = req.user
    data = req.data
    mon = data['mon']
    tue = data['tue']
    wed = data['wed']
    thu = data['thu']
    fri = data['fri']
    sat = data['sat']
    sun = data['sun']
    if user.carer:
        av = Availability.objects.filter(carer__user = user).first()
        if av:
            av.mon = mon
            av.tue = tue
            av.wed = wed 
            av.thu=thu
            av.fri = fri 
            av.sat = sat 
            av.sun = sun
            av.count = data['count']
            av.save()
        else:
            new_av = Availability.objects.create(carer=CarerProfile.objects.filter(user=user).first(),
            mon=mon,
            tue=tue,
            wed=wed,
            thu=thu,
            fri=fri,
            sat=sat,
            sun=sun
            )
            new_av.save()
            return Response(AVSerializer(new_av).data, status=200)
    
        return Response(AVSerializer(av).data, status=200)
    return Response({}, status=400)