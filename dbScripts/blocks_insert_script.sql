-- PostgreSQL Script to Insert All Blocks (Talukas) with District Mapping
-- This script assumes the districts table is already populated

-- Begin transaction for data integrity
BEGIN;

-- Insert blocks with proper district_id mapping using subquery
-- The district_id is fetched from districts table using the district code

INSERT INTO public.blocks (name, district_id, created_at, updated_at, is_active, code)
VALUES 
    -- नंदुरबार District (497) Talukas
    ('अक्कलकुवा', (SELECT id FROM public.districts WHERE code = '497'), NOW(), NOW(), true, '3950'),
    ('अक्राणी', (SELECT id FROM public.districts WHERE code = '497'), NOW(), NOW(), true, '3951'),
    ('तळोदा', (SELECT id FROM public.districts WHERE code = '497'), NOW(), NOW(), true, '3952'),
    ('शहादा', (SELECT id FROM public.districts WHERE code = '497'), NOW(), NOW(), true, '3953'),
    ('नंदुरबार', (SELECT id FROM public.districts WHERE code = '497'), NOW(), NOW(), true, '3954'),
    ('नवापूर', (SELECT id FROM public.districts WHERE code = '497'), NOW(), NOW(), true, '3955'),
    
    -- धुळे District (498) Talukas
    ('शिरपूर', (SELECT id FROM public.districts WHERE code = '498'), NOW(), NOW(), true, '3956'),
    ('सिंदखेडा', (SELECT id FROM public.districts WHERE code = '498'), NOW(), NOW(), true, '3957'),
    ('साक्री', (SELECT id FROM public.districts WHERE code = '498'), NOW(), NOW(), true, '3958'),
    ('धुळे', (SELECT id FROM public.districts WHERE code = '498'), NOW(), NOW(), true, '3959'),
    
    -- जळगाव District (499) Talukas
    ('चोपडा', (SELECT id FROM public.districts WHERE code = '499'), NOW(), NOW(), true, '3960'),
    ('यावल', (SELECT id FROM public.districts WHERE code = '499'), NOW(), NOW(), true, '3961'),
    ('रावेर', (SELECT id FROM public.districts WHERE code = '499'), NOW(), NOW(), true, '3962'),
    ('मुक्ताईनगर (एदलाबाद)', (SELECT id FROM public.districts WHERE code = '499'), NOW(), NOW(), true, '3963'),
    ('बोदवड', (SELECT id FROM public.districts WHERE code = '499'), NOW(), NOW(), true, '3964'),
    ('भुसावळ', (SELECT id FROM public.districts WHERE code = '499'), NOW(), NOW(), true, '3965'),
    ('जळगाव', (SELECT id FROM public.districts WHERE code = '499'), NOW(), NOW(), true, '3966'),
    ('एरंडोल', (SELECT id FROM public.districts WHERE code = '499'), NOW(), NOW(), true, '3967'),
    ('धरणगाव', (SELECT id FROM public.districts WHERE code = '499'), NOW(), NOW(), true, '3968'),
    ('अमळनेर', (SELECT id FROM public.districts WHERE code = '499'), NOW(), NOW(), true, '3969'),
    ('पारोळा', (SELECT id FROM public.districts WHERE code = '499'), NOW(), NOW(), true, '3970'),
    ('भडगाव', (SELECT id FROM public.districts WHERE code = '499'), NOW(), NOW(), true, '3971'),
    ('चाळीसगाव', (SELECT id FROM public.districts WHERE code = '499'), NOW(), NOW(), true, '3972'),
    ('पाचोरा', (SELECT id FROM public.districts WHERE code = '499'), NOW(), NOW(), true, '3973'),
    ('जामनेर', (SELECT id FROM public.districts WHERE code = '499'), NOW(), NOW(), true, '3974'),
    
    -- बुलढाणा District (500) Talukas
    ('जळगाव (जामोद)', (SELECT id FROM public.districts WHERE code = '500'), NOW(), NOW(), true, '3975'),
    ('संग्रामपूर', (SELECT id FROM public.districts WHERE code = '500'), NOW(), NOW(), true, '3976'),
    ('शेगाव', (SELECT id FROM public.districts WHERE code = '500'), NOW(), NOW(), true, '3977'),
    ('नांदुरा', (SELECT id FROM public.districts WHERE code = '500'), NOW(), NOW(), true, '3978'),
    ('मलकापूर', (SELECT id FROM public.districts WHERE code = '500'), NOW(), NOW(), true, '3979'),
    ('मोताळा', (SELECT id FROM public.districts WHERE code = '500'), NOW(), NOW(), true, '3980'),
    ('खामगाव', (SELECT id FROM public.districts WHERE code = '500'), NOW(), NOW(), true, '3981'),
    ('मेहकर', (SELECT id FROM public.districts WHERE code = '500'), NOW(), NOW(), true, '3982'),
    ('चिखली', (SELECT id FROM public.districts WHERE code = '500'), NOW(), NOW(), true, '3983'),
    ('बुलडाणा', (SELECT id FROM public.districts WHERE code = '500'), NOW(), NOW(), true, '3984'),
    ('देऊळगाव राजा', (SELECT id FROM public.districts WHERE code = '500'), NOW(), NOW(), true, '3985'),
    ('सिंदखेड राजा', (SELECT id FROM public.districts WHERE code = '500'), NOW(), NOW(), true, '3986'),
    ('लोणार', (SELECT id FROM public.districts WHERE code = '500'), NOW(), NOW(), true, '3987'),
    
    -- अकोला District (501) Talukas
    ('तेल्हारा', (SELECT id FROM public.districts WHERE code = '501'), NOW(), NOW(), true, '3988'),
    ('अकोट', (SELECT id FROM public.districts WHERE code = '501'), NOW(), NOW(), true, '3989'),
    ('बाळापूर', (SELECT id FROM public.districts WHERE code = '501'), NOW(), NOW(), true, '3990'),
    ('अकोला', (SELECT id FROM public.districts WHERE code = '501'), NOW(), NOW(), true, '3991'),
    ('मूर्तिजापूर', (SELECT id FROM public.districts WHERE code = '501'), NOW(), NOW(), true, '3992'),
    ('पातूर', (SELECT id FROM public.districts WHERE code = '501'), NOW(), NOW(), true, '3993'),
    ('बार्शी टाकळी', (SELECT id FROM public.districts WHERE code = '501'), NOW(), NOW(), true, '3994'),
    
    -- वाशीम District (502) Talukas
    ('मालेगाव', (SELECT id FROM public.districts WHERE code = '502'), NOW(), NOW(), true, '3995'),
    ('मंगरूळपीर', (SELECT id FROM public.districts WHERE code = '502'), NOW(), NOW(), true, '3996'),
    ('कारंजा', (SELECT id FROM public.districts WHERE code = '502'), NOW(), NOW(), true, '3997'),
    ('मनोरा', (SELECT id FROM public.districts WHERE code = '502'), NOW(), NOW(), true, '3998'),
    ('वाशीम', (SELECT id FROM public.districts WHERE code = '502'), NOW(), NOW(), true, '3999'),
    ('रिसोड', (SELECT id FROM public.districts WHERE code = '502'), NOW(), NOW(), true, '4000'),
    
    -- अमरावती District (503) Talukas
    ('धारणी', (SELECT id FROM public.districts WHERE code = '503'), NOW(), NOW(), true, '4001'),
    ('चिखलदरा', (SELECT id FROM public.districts WHERE code = '503'), NOW(), NOW(), true, '4002'),
    ('अंजनगाव सुर्जी', (SELECT id FROM public.districts WHERE code = '503'), NOW(), NOW(), true, '4003'),
    ('अचलपूर', (SELECT id FROM public.districts WHERE code = '503'), NOW(), NOW(), true, '4004'),
    ('चांदूर बाजार', (SELECT id FROM public.districts WHERE code = '503'), NOW(), NOW(), true, '4005'),
    ('मोर्शी', (SELECT id FROM public.districts WHERE code = '503'), NOW(), NOW(), true, '4006'),
    ('वरुड', (SELECT id FROM public.districts WHERE code = '503'), NOW(), NOW(), true, '4007'),
    ('तिवसा', (SELECT id FROM public.districts WHERE code = '503'), NOW(), NOW(), true, '4008'),
    ('अमरावती', (SELECT id FROM public.districts WHERE code = '503'), NOW(), NOW(), true, '4009'),
    ('भातकुली', (SELECT id FROM public.districts WHERE code = '503'), NOW(), NOW(), true, '4010'),
    ('दर्यापूर', (SELECT id FROM public.districts WHERE code = '503'), NOW(), NOW(), true, '4011'),
    ('नांदगाव -खांडेश्वर', (SELECT id FROM public.districts WHERE code = '503'), NOW(), NOW(), true, '4012'),
    ('चांदूर रेल्वे', (SELECT id FROM public.districts WHERE code = '503'), NOW(), NOW(), true, '4013'),
    ('धामणगाव रेल्वे', (SELECT id FROM public.districts WHERE code = '503'), NOW(), NOW(), true, '4014'),
    
    -- वर्धा District (504) Talukas
    ('आष्टी', (SELECT id FROM public.districts WHERE code = '504'), NOW(), NOW(), true, '4015'),
    ('कारंजा', (SELECT id FROM public.districts WHERE code = '504'), NOW(), NOW(), true, '4016'),
    ('आर्वी', (SELECT id FROM public.districts WHERE code = '504'), NOW(), NOW(), true, '4017'),
    ('सेलू', (SELECT id FROM public.districts WHERE code = '504'), NOW(), NOW(), true, '4018'),
    ('वर्धा', (SELECT id FROM public.districts WHERE code = '504'), NOW(), NOW(), true, '4019'),
    ('देवळी', (SELECT id FROM public.districts WHERE code = '504'), NOW(), NOW(), true, '4020'),
    ('हिंगणघाट', (SELECT id FROM public.districts WHERE code = '504'), NOW(), NOW(), true, '4021'),
    ('समुद्रपूर', (SELECT id FROM public.districts WHERE code = '504'), NOW(), NOW(), true, '4022'),
    
    -- नागपूर District (505) Talukas
    ('नरखेड', (SELECT id FROM public.districts WHERE code = '505'), NOW(), NOW(), true, '4023'),
    ('काटोल', (SELECT id FROM public.districts WHERE code = '505'), NOW(), NOW(), true, '4024'),
    ('कळमेश्वर', (SELECT id FROM public.districts WHERE code = '505'), NOW(), NOW(), true, '4025'),
    ('सावनेर', (SELECT id FROM public.districts WHERE code = '505'), NOW(), NOW(), true, '4026'),
    ('पारशिवनी', (SELECT id FROM public.districts WHERE code = '505'), NOW(), NOW(), true, '4027'),
    ('रामटेक', (SELECT id FROM public.districts WHERE code = '505'), NOW(), NOW(), true, '4028'),
    ('मौदा', (SELECT id FROM public.districts WHERE code = '505'), NOW(), NOW(), true, '4029'),
    ('कामठी', (SELECT id FROM public.districts WHERE code = '505'), NOW(), NOW(), true, '4030'),
    ('नागपूर (ग्रामीण)', (SELECT id FROM public.districts WHERE code = '505'), NOW(), NOW(), true, '4031'),
    ('हिंगणा', (SELECT id FROM public.districts WHERE code = '505'), NOW(), NOW(), true, '4033'),
    ('उमरेड', (SELECT id FROM public.districts WHERE code = '505'), NOW(), NOW(), true, '4034'),
    ('कुही', (SELECT id FROM public.districts WHERE code = '505'), NOW(), NOW(), true, '4035'),
    ('भिवापूर', (SELECT id FROM public.districts WHERE code = '505'), NOW(), NOW(), true, '4036'),
    
    -- भंडारा District (506) Talukas
    ('तुमसर', (SELECT id FROM public.districts WHERE code = '506'), NOW(), NOW(), true, '4037'),
    ('मोहाडी', (SELECT id FROM public.districts WHERE code = '506'), NOW(), NOW(), true, '4038'),
    ('भंडारा', (SELECT id FROM public.districts WHERE code = '506'), NOW(), NOW(), true, '4039'),
    ('साकोली', (SELECT id FROM public.districts WHERE code = '506'), NOW(), NOW(), true, '4040'),
    ('लाखनी', (SELECT id FROM public.districts WHERE code = '506'), NOW(), NOW(), true, '4041'),
    ('पवनी', (SELECT id FROM public.districts WHERE code = '506'), NOW(), NOW(), true, '4042'),
    ('लाखांदूर', (SELECT id FROM public.districts WHERE code = '506'), NOW(), NOW(), true, '4043'),
    
    -- गोंदिया District (507) Talukas
    ('तिरोडा', (SELECT id FROM public.districts WHERE code = '507'), NOW(), NOW(), true, '4044'),
    ('गोरेगाव', (SELECT id FROM public.districts WHERE code = '507'), NOW(), NOW(), true, '4045'),
    ('गोंदिया', (SELECT id FROM public.districts WHERE code = '507'), NOW(), NOW(), true, '4046'),
    ('आमगाव', (SELECT id FROM public.districts WHERE code = '507'), NOW(), NOW(), true, '4047'),
    ('सालेकसा', (SELECT id FROM public.districts WHERE code = '507'), NOW(), NOW(), true, '4048'),
    ('सडक अर्जुनी', (SELECT id FROM public.districts WHERE code = '507'), NOW(), NOW(), true, '4049'),
    ('अर्जुनी मोरगाव', (SELECT id FROM public.districts WHERE code = '507'), NOW(), NOW(), true, '4050'),
    ('देवरी', (SELECT id FROM public.districts WHERE code = '507'), NOW(), NOW(), true, '4051'),
    
    -- गडचिरोली District (508) Talukas
    ('देसाईगंज (वादासा)', (SELECT id FROM public.districts WHERE code = '508'), NOW(), NOW(), true, '4052'),
    ('आरमोरी', (SELECT id FROM public.districts WHERE code = '508'), NOW(), NOW(), true, '4053'),
    ('कुरखेडा', (SELECT id FROM public.districts WHERE code = '508'), NOW(), NOW(), true, '4054'),
    ('कोरची', (SELECT id FROM public.districts WHERE code = '508'), NOW(), NOW(), true, '4055'),
    ('धानोरा', (SELECT id FROM public.districts WHERE code = '508'), NOW(), NOW(), true, '4056'),
    ('गडचिरोली', (SELECT id FROM public.districts WHERE code = '508'), NOW(), NOW(), true, '4057'),
    ('चामोर्शी', (SELECT id FROM public.districts WHERE code = '508'), NOW(), NOW(), true, '4058'),
    ('मुलचेरा', (SELECT id FROM public.districts WHERE code = '508'), NOW(), NOW(), true, '4059'),
    ('एटापल्ली', (SELECT id FROM public.districts WHERE code = '508'), NOW(), NOW(), true, '4060'),
    ('भामरागड', (SELECT id FROM public.districts WHERE code = '508'), NOW(), NOW(), true, '4061'),
    ('अहेरी', (SELECT id FROM public.districts WHERE code = '508'), NOW(), NOW(), true, '4062'),
    ('सिरोंचा', (SELECT id FROM public.districts WHERE code = '508'), NOW(), NOW(), true, '4063'),
    
    -- चंद्रपुर District (509) Talukas
    ('वरोरा', (SELECT id FROM public.districts WHERE code = '509'), NOW(), NOW(), true, '4064'),
    ('चिमूर', (SELECT id FROM public.districts WHERE code = '509'), NOW(), NOW(), true, '4065'),
    ('नागभीड', (SELECT id FROM public.districts WHERE code = '509'), NOW(), NOW(), true, '4066'),
    ('ब्रह्मपुरी', (SELECT id FROM public.districts WHERE code = '509'), NOW(), NOW(), true, '4067'),
    ('सावली', (SELECT id FROM public.districts WHERE code = '509'), NOW(), NOW(), true, '4068'),
    ('सिंदेवाही', (SELECT id FROM public.districts WHERE code = '509'), NOW(), NOW(), true, '4069'),
    ('भद्रावती', (SELECT id FROM public.districts WHERE code = '509'), NOW(), NOW(), true, '4070'),
    ('चंद्रपूर', (SELECT id FROM public.districts WHERE code = '509'), NOW(), NOW(), true, '4071'),
    ('मूल', (SELECT id FROM public.districts WHERE code = '509'), NOW(), NOW(), true, '4072'),
    ('पोंभुर्णा', (SELECT id FROM public.districts WHERE code = '509'), NOW(), NOW(), true, '4073'),
    ('बल्लारपूर', (SELECT id FROM public.districts WHERE code = '509'), NOW(), NOW(), true, '4074'),
    ('कोरपना', (SELECT id FROM public.districts WHERE code = '509'), NOW(), NOW(), true, '4075'),
    ('जिवती', (SELECT id FROM public.districts WHERE code = '509'), NOW(), NOW(), true, '4076'),
    ('राजुरा', (SELECT id FROM public.districts WHERE code = '509'), NOW(), NOW(), true, '4077'),
    ('गोंडपिंपरी', (SELECT id FROM public.districts WHERE code = '509'), NOW(), NOW(), true, '4078'),
    
    -- यवतमाळ District (510) Talukas
    ('नेर', (SELECT id FROM public.districts WHERE code = '510'), NOW(), NOW(), true, '4079'),
    ('बाभूळगाव', (SELECT id FROM public.districts WHERE code = '510'), NOW(), NOW(), true, '4080'),
    ('कळंब', (SELECT id FROM public.districts WHERE code = '510'), NOW(), NOW(), true, '4081'),
    ('यवतमाळ', (SELECT id FROM public.districts WHERE code = '510'), NOW(), NOW(), true, '4082'),
    ('दारव्हा', (SELECT id FROM public.districts WHERE code = '510'), NOW(), NOW(), true, '4083'),
    ('दिग्रस', (SELECT id FROM public.districts WHERE code = '510'), NOW(), NOW(), true, '4084'),
    ('पुसद', (SELECT id FROM public.districts WHERE code = '510'), NOW(), NOW(), true, '4085'),
    ('उमरखेड', (SELECT id FROM public.districts WHERE code = '510'), NOW(), NOW(), true, '4086'),
    ('महागाव', (SELECT id FROM public.districts WHERE code = '510'), NOW(), NOW(), true, '4087'),
    ('आर्णी', (SELECT id FROM public.districts WHERE code = '510'), NOW(), NOW(), true, '4088'),
    ('घाटंजी', (SELECT id FROM public.districts WHERE code = '510'), NOW(), NOW(), true, '4089'),
    ('केळापूर', (SELECT id FROM public.districts WHERE code = '510'), NOW(), NOW(), true, '4090'),
    ('राळेगाव', (SELECT id FROM public.districts WHERE code = '510'), NOW(), NOW(), true, '4091'),
    ('मोरेगाव', (SELECT id FROM public.districts WHERE code = '510'), NOW(), NOW(), true, '4092'),
    ('झरी जामडी', (SELECT id FROM public.districts WHERE code = '510'), NOW(), NOW(), true, '4093'),
    ('वणी', (SELECT id FROM public.districts WHERE code = '510'), NOW(), NOW(), true, '4094'),
    
    -- नांदेड District (511) Talukas
    ('माहूर', (SELECT id FROM public.districts WHERE code = '511'), NOW(), NOW(), true, '4095'),
    ('किनवट', (SELECT id FROM public.districts WHERE code = '511'), NOW(), NOW(), true, '4096'),
    ('हिमायतनगर', (SELECT id FROM public.districts WHERE code = '511'), NOW(), NOW(), true, '4097'),
    ('हदगाव', (SELECT id FROM public.districts WHERE code = '511'), NOW(), NOW(), true, '4098'),
    ('अर्धापूर', (SELECT id FROM public.districts WHERE code = '511'), NOW(), NOW(), true, '4099'),
    ('नांदेड', (SELECT id FROM public.districts WHERE code = '511'), NOW(), NOW(), true, '4100'),
    ('मुदखेड', (SELECT id FROM public.districts WHERE code = '511'), NOW(), NOW(), true, '4101'),
    ('भोकर', (SELECT id FROM public.districts WHERE code = '511'), NOW(), NOW(), true, '4102'),
    ('उमरी', (SELECT id FROM public.districts WHERE code = '511'), NOW(), NOW(), true, '4103'),
    ('धर्माबाद', (SELECT id FROM public.districts WHERE code = '511'), NOW(), NOW(), true, '4104'),
    ('बिलोली', (SELECT id FROM public.districts WHERE code = '511'), NOW(), NOW(), true, '4105'),
    ('नायगाव (खैरगाव)', (SELECT id FROM public.districts WHERE code = '511'), NOW(), NOW(), true, '4106'),
    ('लोहा', (SELECT id FROM public.districts WHERE code = '511'), NOW(), NOW(), true, '4107'),
    ('कंधार', (SELECT id FROM public.districts WHERE code = '511'), NOW(), NOW(), true, '4108'),
    ('मुखेड', (SELECT id FROM public.districts WHERE code = '511'), NOW(), NOW(), true, '4109'),
    ('देगलूर', (SELECT id FROM public.districts WHERE code = '511'), NOW(), NOW(), true, '4110'),
    
    -- हिंगोली District (512) Talukas
    ('सेनगाव', (SELECT id FROM public.districts WHERE code = '512'), NOW(), NOW(), true, '4111'),
    ('हिंगोली', (SELECT id FROM public.districts WHERE code = '512'), NOW(), NOW(), true, '4112'),
    ('औंढा (नागनाथ)', (SELECT id FROM public.districts WHERE code = '512'), NOW(), NOW(), true, '4113'),
    ('कळमनुरी', (SELECT id FROM public.districts WHERE code = '512'), NOW(), NOW(), true, '4114'),
    ('बसमत', (SELECT id FROM public.districts WHERE code = '512'), NOW(), NOW(), true, '4115'),
    
    -- परभणी District (513) Talukas
    ('सेलू', (SELECT id FROM public.districts WHERE code = '513'), NOW(), NOW(), true, '4116'),
    ('जिंतूर', (SELECT id FROM public.districts WHERE code = '513'), NOW(), NOW(), true, '4117'),
    ('परभणी', (SELECT id FROM public.districts WHERE code = '513'), NOW(), NOW(), true, '4118'),
    ('मानवत', (SELECT id FROM public.districts WHERE code = '513'), NOW(), NOW(), true, '4119'),
    ('पाथ्री', (SELECT id FROM public.districts WHERE code = '513'), NOW(), NOW(), true, '4120'),
    ('सोनपेठ', (SELECT id FROM public.districts WHERE code = '513'), NOW(), NOW(), true, '4121'),
    ('गंगाखेड', (SELECT id FROM public.districts WHERE code = '513'), NOW(), NOW(), true, '4122'),
    ('पालम', (SELECT id FROM public.districts WHERE code = '513'), NOW(), NOW(), true, '4123'),
    ('पूर्णा', (SELECT id FROM public.districts WHERE code = '513'), NOW(), NOW(), true, '4124'),
    
    -- जालना District (514) Talukas
    ('भोकरदन', (SELECT id FROM public.districts WHERE code = '514'), NOW(), NOW(), true, '4125'),
    ('जाफ्राबाद', (SELECT id FROM public.districts WHERE code = '514'), NOW(), NOW(), true, '4126'),
    ('जालना', (SELECT id FROM public.districts WHERE code = '514'), NOW(), NOW(), true, '4127'),
    ('बदनापूर', (SELECT id FROM public.districts WHERE code = '514'), NOW(), NOW(), true, '4128'),
    ('अंबड', (SELECT id FROM public.districts WHERE code = '514'), NOW(), NOW(), true, '4129'),
    ('घनसावंगी', (SELECT id FROM public.districts WHERE code = '514'), NOW(), NOW(), true, '4130'),
    ('परतूर', (SELECT id FROM public.districts WHERE code = '514'), NOW(), NOW(), true, '4131'),
    ('मंठा', (SELECT id FROM public.districts WHERE code = '514'), NOW(), NOW(), true, '4132'),
    
    -- औरंगाबाद District (515) Talukas
    ('कन्नड', (SELECT id FROM public.districts WHERE code = '515'), NOW(), NOW(), true, '4133'),
    ('सोयगाव', (SELECT id FROM public.districts WHERE code = '515'), NOW(), NOW(), true, '4134'),
    ('सिल्लोड', (SELECT id FROM public.districts WHERE code = '515'), NOW(), NOW(), true, '4135'),
    ('फुलंब्री', (SELECT id FROM public.districts WHERE code = '515'), NOW(), NOW(), true, '4136'),
    ('औरंगाबाद', (SELECT id FROM public.districts WHERE code = '515'), NOW(), NOW(), true, '4137'),
    ('खुलदाबाद', (SELECT id FROM public.districts WHERE code = '515'), NOW(), NOW(), true, '4138'),
    ('वैजापूर', (SELECT id FROM public.districts WHERE code = '515'), NOW(), NOW(), true, '4139'),
    ('गंगापूर', (SELECT id FROM public.districts WHERE code = '515'), NOW(), NOW(), true, '4140'),
    ('पैठण', (SELECT id FROM public.districts WHERE code = '515'), NOW(), NOW(), true, '4141'),
    
    -- नाशिक District (516) Talukas
    ('सुरगाणा', (SELECT id FROM public.districts WHERE code = '516'), NOW(), NOW(), true, '4142'),
    ('कळवण', (SELECT id FROM public.districts WHERE code = '516'), NOW(), NOW(), true, '4143'),
    ('देवळा', (SELECT id FROM public.districts WHERE code = '516'), NOW(), NOW(), true, '4144'),
    ('बागलाण', (SELECT id FROM public.districts WHERE code = '516'), NOW(), NOW(), true, '4145'),
    ('मालेगाव', (SELECT id FROM public.districts WHERE code = '516'), NOW(), NOW(), true, '4146'),
    ('नांदगाव', (SELECT id FROM public.districts WHERE code = '516'), NOW(), NOW(), true, '4147'),
    ('चांदवड', (SELECT id FROM public.districts WHERE code = '516'), NOW(), NOW(), true, '4148'),
    ('दिंडोरी', (SELECT id FROM public.districts WHERE code = '516'), NOW(), NOW(), true, '4149'),
    ('पेठ', (SELECT id FROM public.districts WHERE code = '516'), NOW(), NOW(), true, '4150'),
    ('त्र्यंबकेश्वर', (SELECT id FROM public.districts WHERE code = '516'), NOW(), NOW(), true, '4151'),
    ('नाशिक', (SELECT id FROM public.districts WHERE code = '516'), NOW(), NOW(), true, '4152'),
    ('इगतपुरी', (SELECT id FROM public.districts WHERE code = '516'), NOW(), NOW(), true, '4153'),
    ('सिन्नर', (SELECT id FROM public.districts WHERE code = '516'), NOW(), NOW(), true, '4154'),
    ('निफाड', (SELECT id FROM public.districts WHERE code = '516'), NOW(), NOW(), true, '4155'),
    ('येवले', (SELECT id FROM public.districts WHERE code = '516'), NOW(), NOW(), true, '4156'),
    
    -- पालघर District (532) Talukas
    ('तलासरी', (SELECT id FROM public.districts WHERE code = '532'), NOW(), NOW(), true, '4157'),
    ('डहाणू', (SELECT id FROM public.districts WHERE code = '532'), NOW(), NOW(), true, '4158'),
    ('विक्रमगड', (SELECT id FROM public.districts WHERE code = '532'), NOW(), NOW(), true, '4159'),
    ('जव्हार', (SELECT id FROM public.districts WHERE code = '532'), NOW(), NOW(), true, '4160'),
    ('मोखाडा', (SELECT id FROM public.districts WHERE code = '532'), NOW(), NOW(), true, '4161'),
    ('वाडा', (SELECT id FROM public.districts WHERE code = '532'), NOW(), NOW(), true, '4162'),
    ('पालघर', (SELECT id FROM public.districts WHERE code = '532'), NOW(), NOW(), true, '4163'),
    ('वसई', (SELECT id FROM public.districts WHERE code = '532'), NOW(), NOW(), true, '4164'),
    
    -- ठाणे District (517) Talukas
    ('भिवंडी', (SELECT id FROM public.districts WHERE code = '517'), NOW(), NOW(), true, '4166'),
    ('शहापूर', (SELECT id FROM public.districts WHERE code = '517'), NOW(), NOW(), true, '4167'),
    ('कल्याण', (SELECT id FROM public.districts WHERE code = '517'), NOW(), NOW(), true, '4168'),
    ('अंबरनाथ', (SELECT id FROM public.districts WHERE code = '517'), NOW(), NOW(), true, '4170'),
    ('मुरबाड', (SELECT id FROM public.districts WHERE code = '517'), NOW(), NOW(), true, '4171'),
    
    -- रायगड District (520) Talukas
    ('उरण', (SELECT id FROM public.districts WHERE code = '520'), NOW(), NOW(), true, '4172'),
    ('पनवेल', (SELECT id FROM public.districts WHERE code = '520'), NOW(), NOW(), true, '4173'),
    ('कर्जत', (SELECT id FROM public.districts WHERE code = '520'), NOW(), NOW(), true, '4174'),
    ('खालापूर', (SELECT id FROM public.districts WHERE code = '520'), NOW(), NOW(), true, '4175'),
    ('पेण', (SELECT id FROM public.districts WHERE code = '520'), NOW(), NOW(), true, '4176'),
    ('अलिबाग', (SELECT id FROM public.districts WHERE code = '520'), NOW(), NOW(), true, '4177'),
    ('मुरुड', (SELECT id FROM public.districts WHERE code = '520'), NOW(), NOW(), true, '4178'),
    ('रोहा', (SELECT id FROM public.districts WHERE code = '520'), NOW(), NOW(), true, '4179'),
    ('सुधागड', (SELECT id FROM public.districts WHERE code = '520'), NOW(), NOW(), true, '4180'),
    ('माणगाव', (SELECT id FROM public.districts WHERE code = '520'), NOW(), NOW(), true, '4181'),
    ('तळा', (SELECT id FROM public.districts WHERE code = '520'), NOW(), NOW(), true, '4182'),
    ('श्रीवर्धन', (SELECT id FROM public.districts WHERE code = '520'), NOW(), NOW(), true, '4183'),
    ('म्हसळा', (SELECT id FROM public.districts WHERE code = '520'), NOW(), NOW(), true, '4184'),
    ('महाड', (SELECT id FROM public.districts WHERE code = '520'), NOW(), NOW(), true, '4185'),
    ('पोलादपूर', (SELECT id FROM public.districts WHERE code = '520'), NOW(), NOW(), true, '4186'),
    
    -- पुणे District (521) Talukas
    ('जुन्नर', (SELECT id FROM public.districts WHERE code = '521'), NOW(), NOW(), true, '4187'),
    ('आंबेगाव', (SELECT id FROM public.districts WHERE code = '521'), NOW(), NOW(), true, '4188'),
    ('शिरूर', (SELECT id FROM public.districts WHERE code = '521'), NOW(), NOW(), true, '4189'),
    ('खेड', (SELECT id FROM public.districts WHERE code = '521'), NOW(), NOW(), true, '4190'),
    ('मावळ', (SELECT id FROM public.districts WHERE code = '521'), NOW(), NOW(), true, '4191'),
    ('मुळशी', (SELECT id FROM public.districts WHERE code = '521'), NOW(), NOW(), true, '4192'),
    ('हवेली', (SELECT id FROM public.districts WHERE code = '521'), NOW(), NOW(), true, '4193'),
    ('दौंड', (SELECT id FROM public.districts WHERE code = '521'), NOW(), NOW(), true, '4195'),
    ('पुरंदर', (SELECT id FROM public.districts WHERE code = '521'), NOW(), NOW(), true, '4196'),
    ('वेल्हे', (SELECT id FROM public.districts WHERE code = '521'), NOW(), NOW(), true, '4197'),
    ('भोर', (SELECT id FROM public.districts WHERE code = '521'), NOW(), NOW(), true, '4198'),
    ('बारामती', (SELECT id FROM public.districts WHERE code = '521'), NOW(), NOW(), true, '4199'),
    ('इंदापूर', (SELECT id FROM public.districts WHERE code = '521'), NOW(), NOW(), true, '4200'),
    
    -- अहमदनगर District (522) Talukas
    ('अकोले', (SELECT id FROM public.districts WHERE code = '522'), NOW(), NOW(), true, '4201'),
    ('संगमनेर', (SELECT id FROM public.districts WHERE code = '522'), NOW(), NOW(), true, '4202'),
    ('कोपरगाव', (SELECT id FROM public.districts WHERE code = '522'), NOW(), NOW(), true, '4203'),
    ('रहाता', (SELECT id FROM public.districts WHERE code = '522'), NOW(), NOW(), true, '4204'),
    ('श्रीरामपूर', (SELECT id FROM public.districts WHERE code = '522'), NOW(), NOW(), true, '4205'),
    ('नेवासा', (SELECT id FROM public.districts WHERE code = '522'), NOW(), NOW(), true, '4206'),
    ('शेवगाव', (SELECT id FROM public.districts WHERE code = '522'), NOW(), NOW(), true, '4207'),
    ('पाथर्डी', (SELECT id FROM public.districts WHERE code = '522'), NOW(), NOW(), true, '4208'),
    ('नगर', (SELECT id FROM public.districts WHERE code = '522'), NOW(), NOW(), true, '4209'),
    ('राहुरी', (SELECT id FROM public.districts WHERE code = '522'), NOW(), NOW(), true, '4210'),
    ('पारनेर', (SELECT id FROM public.districts WHERE code = '522'), NOW(), NOW(), true, '4211'),
    ('श्रीगोंदे', (SELECT id FROM public.districts WHERE code = '522'), NOW(), NOW(), true, '4212'),
    ('कर्जत', (SELECT id FROM public.districts WHERE code = '522'), NOW(), NOW(), true, '4213'),
    ('जामखेड', (SELECT id FROM public.districts WHERE code = '522'), NOW(), NOW(), true, '4214'),
    
    -- बीड District (523) Talukas
    ('आष्टी', (SELECT id FROM public.districts WHERE code = '523'), NOW(), NOW(), true, '4215'),
    ('पाटोदा', (SELECT id FROM public.districts WHERE code = '523'), NOW(), NOW(), true, '4216'),
    ('शिरूर (कासार)', (SELECT id FROM public.districts WHERE code = '523'), NOW(), NOW(), true, '4217'),
    ('गेवराई', (SELECT id FROM public.districts WHERE code = '523'), NOW(), NOW(), true, '4218'),
    ('माजलगाव', (SELECT id FROM public.districts WHERE code = '523'), NOW(), NOW(), true, '4219'),
    ('वडवणी', (SELECT id FROM public.districts WHERE code = '523'), NOW(), NOW(), true, '4220'),
    ('बीड', (SELECT id FROM public.districts WHERE code = '523'), NOW(), NOW(), true, '4221'),
    ('केज', (SELECT id FROM public.districts WHERE code = '523'), NOW(), NOW(), true, '4222'),
    ('धारूर', (SELECT id FROM public.districts WHERE code = '523'), NOW(), NOW(), true, '4223'),
    ('परळी', (SELECT id FROM public.districts WHERE code = '523'), NOW(), NOW(), true, '4224'),
    ('अंबेजोगाई', (SELECT id FROM public.districts WHERE code = '523'), NOW(), NOW(), true, '4225'),
    
    -- लातूर District (524) Talukas
    ('लातूर', (SELECT id FROM public.districts WHERE code = '524'), NOW(), NOW(), true, '4226'),
    ('रेणापूर', (SELECT id FROM public.districts WHERE code = '524'), NOW(), NOW(), true, '4227'),
    ('अहमदपूर', (SELECT id FROM public.districts WHERE code = '524'), NOW(), NOW(), true, '4228'),
    ('जळकोट', (SELECT id FROM public.districts WHERE code = '524'), NOW(), NOW(), true, '4229'),
    ('चाकूर', (SELECT id FROM public.districts WHERE code = '524'), NOW(), NOW(), true, '4230'),
    ('शिरूर (अनंतपाळ)', (SELECT id FROM public.districts WHERE code = '524'), NOW(), NOW(), true, '4231'),
    ('औसा', (SELECT id FROM public.districts WHERE code = '524'), NOW(), NOW(), true, '4232'),
    ('निलंगा', (SELECT id FROM public.districts WHERE code = '524'), NOW(), NOW(), true, '4233'),
    ('देवणी', (SELECT id FROM public.districts WHERE code = '524'), NOW(), NOW(), true, '4234'),
    ('उदगीर', (SELECT id FROM public.districts WHERE code = '524'), NOW(), NOW(), true, '4235'),
    
    -- उस्मानाबाद District (525) Talukas
    ('परांडा', (SELECT id FROM public.districts WHERE code = '525'), NOW(), NOW(), true, '4236'),
    ('भूम', (SELECT id FROM public.districts WHERE code = '525'), NOW(), NOW(), true, '4237'),
    ('वाशी', (SELECT id FROM public.districts WHERE code = '525'), NOW(), NOW(), true, '4238'),
    ('कळंब', (SELECT id FROM public.districts WHERE code = '525'), NOW(), NOW(), true, '4239'),
    ('उस्मानाबाद', (SELECT id FROM public.districts WHERE code = '525'), NOW(), NOW(), true, '4240'),
    ('तुळजापूर', (SELECT id FROM public.districts WHERE code = '525'), NOW(), NOW(), true, '4241'),
    ('लोहारा', (SELECT id FROM public.districts WHERE code = '525'), NOW(), NOW(), true, '4242'),
    ('उमरगा', (SELECT id FROM public.districts WHERE code = '525'), NOW(), NOW(), true, '4243'),
    
    -- सोलापूर District (526) Talukas
    ('करमाळा', (SELECT id FROM public.districts WHERE code = '526'), NOW(), NOW(), true, '4244'),
    ('माढा', (SELECT id FROM public.districts WHERE code = '526'), NOW(), NOW(), true, '4245'),
    ('बार्शी', (SELECT id FROM public.districts WHERE code = '526'), NOW(), NOW(), true, '4246'),
    ('सोलापूर उत्तर', (SELECT id FROM public.districts WHERE code = '526'), NOW(), NOW(), true, '4247'),
    ('मोहोळ', (SELECT id FROM public.districts WHERE code = '526'), NOW(), NOW(), true, '4248'),
    ('पंढरपूर', (SELECT id FROM public.districts WHERE code = '526'), NOW(), NOW(), true, '4249'),
    ('माळशिरस', (SELECT id FROM public.districts WHERE code = '526'), NOW(), NOW(), true, '4250'),
    ('सांगोले', (SELECT id FROM public.districts WHERE code = '526'), NOW(), NOW(), true, '4251'),
    ('मंगळवेढे', (SELECT id FROM public.districts WHERE code = '526'), NOW(), NOW(), true, '4252'),
    ('सोलापूर दक्षिण', (SELECT id FROM public.districts WHERE code = '526'), NOW(), NOW(), true, '4253'),
    ('अक्कलकोट', (SELECT id FROM public.districts WHERE code = '526'), NOW(), NOW(), true, '4254'),
    
    -- सातारा District (527) Talukas
    ('महाबळेश्वर', (SELECT id FROM public.districts WHERE code = '527'), NOW(), NOW(), true, '4255'),
    ('वाई', (SELECT id FROM public.districts WHERE code = '527'), NOW(), NOW(), true, '4256'),
    ('खंडाला', (SELECT id FROM public.districts WHERE code = '527'), NOW(), NOW(), true, '4257'),
    ('फलटण', (SELECT id FROM public.districts WHERE code = '527'), NOW(), NOW(), true, '4258'),
    ('माण', (SELECT id FROM public.districts WHERE code = '527'), NOW(), NOW(), true, '4259'),
    ('खटाव', (SELECT id FROM public.districts WHERE code = '527'), NOW(), NOW(), true, '4260'),
    ('कोरेगाव', (SELECT id FROM public.districts WHERE code = '527'), NOW(), NOW(), true, '4261'),
    ('सातारा', (SELECT id FROM public.districts WHERE code = '527'), NOW(), NOW(), true, '4262'),
    ('जावळी', (SELECT id FROM public.districts WHERE code = '527'), NOW(), NOW(), true, '4263'),
    ('पाटण', (SELECT id FROM public.districts WHERE code = '527'), NOW(), NOW(), true, '4264'),
    ('कराड', (SELECT id FROM public.districts WHERE code = '527'), NOW(), NOW(), true, '4265'),
    
    -- रत्नागिरी District (528) Talukas
    ('मंडणगड', (SELECT id FROM public.districts WHERE code = '528'), NOW(), NOW(), true, '4266'),
    ('दापोली', (SELECT id FROM public.districts WHERE code = '528'), NOW(), NOW(), true, '4267'),
    ('खेड', (SELECT id FROM public.districts WHERE code = '528'), NOW(), NOW(), true, '4268'),
    ('चिपळूण', (SELECT id FROM public.districts WHERE code = '528'), NOW(), NOW(), true, '4269'),
    ('गुहागर', (SELECT id FROM public.districts WHERE code = '528'), NOW(), NOW(), true, '4270'),
    ('रत्नागिरी', (SELECT id FROM public.districts WHERE code = '528'), NOW(), NOW(), true, '4271'),
    ('संगमेश्वर', (SELECT id FROM public.districts WHERE code = '528'), NOW(), NOW(), true, '4272'),
    ('लांजा', (SELECT id FROM public.districts WHERE code = '528'), NOW(), NOW(), true, '4273'),
    ('राजापूर', (SELECT id FROM public.districts WHERE code = '528'), NOW(), NOW(), true, '4274'),
    
    -- सिंधुदुर्ग District (529) Talukas
    ('देवगड', (SELECT id FROM public.districts WHERE code = '529'), NOW(), NOW(), true, '4275'),
    ('वैभववाडी', (SELECT id FROM public.districts WHERE code = '529'), NOW(), NOW(), true, '4276'),
    ('कणकवली', (SELECT id FROM public.districts WHERE code = '529'), NOW(), NOW(), true, '4277'),
    ('मालवण', (SELECT id FROM public.districts WHERE code = '529'), NOW(), NOW(), true, '4278'),
    ('वेंगुर्ला', (SELECT id FROM public.districts WHERE code = '529'), NOW(), NOW(), true, '4279'),
    ('कुडाळ', (SELECT id FROM public.districts WHERE code = '529'), NOW(), NOW(), true, '4280'),
    ('सावंतवाडी', (SELECT id FROM public.districts WHERE code = '529'), NOW(), NOW(), true, '4281'),
    ('दोडामार्ग', (SELECT id FROM public.districts WHERE code = '529'), NOW(), NOW(), true, '4282'),
    
    -- कोल्हापूर District (530) Talukas
    ('शाहूवाडी', (SELECT id FROM public.districts WHERE code = '530'), NOW(), NOW(), true, '4283'),
    ('पन्हाळा', (SELECT id FROM public.districts WHERE code = '530'), NOW(), NOW(), true, '4284'),
    ('हातकणंगले', (SELECT id FROM public.districts WHERE code = '530'), NOW(), NOW(), true, '4285'),
    ('शिरोळ', (SELECT id FROM public.districts WHERE code = '530'), NOW(), NOW(), true, '4286'),
    ('करवीर', (SELECT id FROM public.districts WHERE code = '530'), NOW(), NOW(), true, '4287'),
    ('गगनबावडा', (SELECT id FROM public.districts WHERE code = '530'), NOW(), NOW(), true, '4288'),
    ('राधानगरी', (SELECT id FROM public.districts WHERE code = '530'), NOW(), NOW(), true, '4289'),
    ('कागल', (SELECT id FROM public.districts WHERE code = '530'), NOW(), NOW(), true, '4290'),
    ('भुदरगड', (SELECT id FROM public.districts WHERE code = '530'), NOW(), NOW(), true, '4291'),
    ('आजरा', (SELECT id FROM public.districts WHERE code = '530'), NOW(), NOW(), true, '4292'),
    ('गडहिंग्लज', (SELECT id FROM public.districts WHERE code = '530'), NOW(), NOW(), true, '4293'),
    ('चंदगड', (SELECT id FROM public.districts WHERE code = '530'), NOW(), NOW(), true, '4294'),
    
    -- सांगली District (531) Talukas
    ('शिराळा', (SELECT id FROM public.districts WHERE code = '531'), NOW(), NOW(), true, '4295'),
    ('वाळवा', (SELECT id FROM public.districts WHERE code = '531'), NOW(), NOW(), true, '4296'),
    ('पलूस', (SELECT id FROM public.districts WHERE code = '531'), NOW(), NOW(), true, '4297'),
    ('कडेगाव', (SELECT id FROM public.districts WHERE code = '531'), NOW(), NOW(), true, '4298'),
    ('खानापूर', (SELECT id FROM public.districts WHERE code = '531'), NOW(), NOW(), true, '4299'),
    ('आटपाडी', (SELECT id FROM public.districts WHERE code = '531'), NOW(), NOW(), true, '4300'),
    ('तासगाव', (SELECT id FROM public.districts WHERE code = '531'), NOW(), NOW(), true, '4301'),
    ('मिरज', (SELECT id FROM public.districts WHERE code = '531'), NOW(), NOW(), true, '4302'),
    ('कवठे महांकाळ', (SELECT id FROM public.districts WHERE code = '531'), NOW(), NOW(), true, '4303'),
    ('जत', (SELECT id FROM public.districts WHERE code = '531'), NOW(), NOW(), true, '4304')

ON CONFLICT (code) DO NOTHING;  -- Prevents duplicate entries based on unique code constraint

-- Commit the transaction
COMMIT;

-- Verification queries to check inserted data
SELECT 
    b.id,
    b.name as block_name,
    d.name as district_name,
    b.code as block_code,
    d.code as district_code,
    b.created_at,
    b.is_active
FROM public.blocks b
JOIN public.districts d ON b.district_id = d.id
ORDER BY d.code, b.code;

-- Count blocks by district
SELECT 
    d.name as district_name,
    d.code as district_code,
    COUNT(b.id) as total_blocks
FROM public.districts d
LEFT JOIN public.blocks b ON d.id = b.district_id
GROUP BY d.name, d.code
ORDER BY d.code;

-- Total count of blocks
SELECT COUNT(*) as total_blocks FROM public.blocks;

-- Check for any blocks without district mapping (should return 0)
SELECT * FROM public.blocks WHERE district_id IS NULL;

-- Check for any duplicate block codes (should return 0)
SELECT code, COUNT(*) as count
FROM public.blocks 
GROUP BY code 
HAVING COUNT(*) > 1;

-- Check for any duplicate block names within same district (should return 0)
SELECT 
    b1.name, 
    d.name as district_name,
    COUNT(*) as count
FROM public.blocks b1
JOIN public.districts d ON b1.district_id = d.id
GROUP BY b1.name, d.name, b1.district_id
HAVING COUNT(*) > 1;