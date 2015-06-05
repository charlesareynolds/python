import unittest
import unum
__author__ = 'reynolds12'


class TestSetenv(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        super(TestSetenv, self).__init__(methodName)
        self.old_e = 0
        self.old_f = 0

    def setUp(self):
        self.old_e = unum.esizesize
        self.old_f = unum.fsizesize

    def tearDown(self):
        unum.setenv ((self.old_e, self.old_f))

    def test_setenv_0_0(self):
        unum.setenv((0, 0))
        self.assertEqual (unum.esizesize, 0)
        self.assertEqual (unum.fsizesize, 0)
        self.assertEqual (unum.esizemax, 1)
        self.assertEqual (unum.fsizemax, 1)
        self.assertEqual (unum.utagsize, 1)
        self.assertEqual (unum.maxubits, 4)
        self.assertEqual (unum.ubitmask, 1)
        self.assertEqual (unum.fsizemask, 0)
        self.assertEqual (unum.esizemask, 0)
        self.assertEqual (unum.efsizemask, 0)
        self.assertEqual (unum.utagmask, 1)
        self.assertEqual (unum.ulpu, 2)
        self.assertEqual (unum.smallsubnormalu, 2)
        self.assertEqual (unum.smallnormalu, 4)
        self.assertEqual (unum.signbigu, 8)
        self.assertEqual (unum.posinfu,  6)
        self.assertEqual (unum.maxrealu, 4)
        self.assertEqual (unum.minrealu, 12)
        self.assertEqual (unum.neginfu, 14)
        self.assertEqual (unum.negbigu, 12)
        self.assertEqual (unum.qNaNu, 7)
        self.assertEqual (unum.sNaNu, 15)
        self.assertEqual (unum.negopeninfu, 13)
        self.assertEqual (unum.posopeninfu, 5)
        self.assertEqual (unum.negopenzerou, 9)
        self.assertEqual (unum.maxreal, 2)
        self.assertEqual (unum.smallsubnormal, 1)

    def test_setenv_0_1(self):
        unum.setenv((0, 1))
        self.assertEqual (unum.esizesize, 0)
        self.assertEqual (unum.fsizesize, 1)
        self.assertEqual (unum.esizemax, 1)
        self.assertEqual (unum.fsizemax, 2)
        self.assertEqual (unum.utagsize, 2)
        self.assertEqual (unum.maxubits, 6)
        self.assertEqual (unum.ubitmask, 2)
        self.assertEqual (unum.fsizemask, 1)
        self.assertEqual (unum.esizemask, 0)
        self.assertEqual (unum.efsizemask, 1)
        self.assertEqual (unum.utagmask, 3)
        self.assertEqual (unum.ulpu, 4)
        self.assertEqual (unum.smallsubnormalu, 5)
        self.assertEqual (unum.smallnormalu, 17)
        self.assertEqual (unum.signbigu, 32)
        self.assertEqual (unum.posinfu,  29)
        self.assertEqual (unum.maxrealu, 25)
        self.assertEqual (unum.minrealu, 57)
        self.assertEqual (unum.neginfu, 61)
        self.assertEqual (unum.negbigu, 57)
        self.assertEqual (unum.qNaNu, 31)
        self.assertEqual (unum.sNaNu, 63)
        self.assertEqual (unum.negopeninfu, 30)
        self.assertEqual (unum.posopeninfu, 14)
        self.assertEqual (unum.negopenzerou, 18)
        self.assertEqual (unum.maxreal, 3)
        self.assertEqual (unum.smallsubnormal, 0.5)

    def test_setenv_4_11(self):
        unum.setenv((4, 11))
        self.assertEqual (unum.esizesize, 4)
        self.assertEqual (unum.fsizesize, 11)
        self.assertEqual (unum.esizemax, 16)
        self.assertEqual (unum.fsizemax, 2048)
        self.assertEqual (unum.utagsize, 16)
        self.assertEqual (unum.maxubits, 2081)
        self.assertEqual (unum.ubitmask, 32768)
        self.assertEqual (unum.fsizemask, 2047)
        self.assertEqual (unum.esizemask, 30720)
        self.assertEqual (unum.efsizemask, 32767)
        self.assertEqual (unum.utagmask, 65535)
        self.assertEqual (unum.ulpu, 65536)
        self.assertEqual (unum.smallsubnormalu, 98303)
        self.assertEqual (unum.smallnormalu, 2117927309889438174459650158668673971679664712562473961529694317938255799180846097576571791705565656756303820286977508605566619428486573004887697154798274682593665179143438079868940959769536240470986433389138252154587854840962728339822221350566374307960038742559051287290680173628035288832904554028985901745564177753025304488882010507612295626414894352651145842398187071689918132565341655148151347141946711521751440013293116283787565541117240665991000726780856711985700908873208313264547895818776171214908852966565917355871174476978782118754092657304498165222185509547752135370035591813854143984012876422254401698572304383L)
        self.assertEqual (unum.signbigu, 138800484180914220201387632798510217407998506602494293542810046820401532055115929850778208941215950881181127166327358003974413970865296048448320120736859729598458441180344358002290914739456327055506566898590564493203069654857333364478589098430717906646469099032349985163882015858886920688953232852843620056797293953222266354983371440626879406172726516295345493927407587930270474735802230711789246686294619686289502372711177668774301895302659484286386223630310225476694894763914580018105410900379315156740266588016863959834373290523281464934668216389107591756001149553721483943610652545112745180136267869208864469717632392626176L)
        self.assertEqual (unum.posinfu,  138800484180914220201387632798510217407998506602494293542810046820401532055115929850778208941215950881181127166327358003974413970865296048448320120736859729598458441180344358002290914739456327055506566898590564493203069654857333364478589098430717906646469099032349985163882015858886920688953232852843620056797293953222266354983371440626879406172726516295345493927407587930270474735802230711789246686294619686289502372711177668774301895302659484286386223630310225476694894763914580018105410900379315156740266588016863959834373290523281464934668216389107591756001149553721483943610652545112745180136267869208864469717632392593407L)
        self.assertEqual (unum.maxrealu, 138800484180914220201387632798510217407998506602494293542810046820401532055115929850778208941215950881181127166327358003974413970865296048448320120736859729598458441180344358002290914739456327055506566898590564493203069654857333364478589098430717906646469099032349985163882015858886920688953232852843620056797293953222266354983371440626879406172726516295345493927407587930270474735802230711789246686294619686289502372711177668774301895302659484286386223630310225476694894763914580018105410900379315156740266588016863959834373290523281464934668216389107591756001149553721483943610652545112745180136267869208864469717632392527871L)
        self.assertEqual (unum.minrealu, 277600968361828440402775265597020434815997013204988587085620093640803064110231859701556417882431901762362254332654716007948827941730592096896640241473719459196916882360688716004581829478912654111013133797181128986406139309714666728957178196861435813292938198064699970327764031717773841377906465705687240113594587906444532709966742881253758812345453032590690987854815175860540949471604461423578493372589239372579004745422355337548603790605318968572772447260620450953389789527829160036210821800758630313480533176033727919668746581046562929869336432778215183512002299107442967887221305090225490360272535738417728939435264785154047L)
        self.assertEqual (unum.neginfu, 277600968361828440402775265597020434815997013204988587085620093640803064110231859701556417882431901762362254332654716007948827941730592096896640241473719459196916882360688716004581829478912654111013133797181128986406139309714666728957178196861435813292938198064699970327764031717773841377906465705687240113594587906444532709966742881253758812345453032590690987854815175860540949471604461423578493372589239372579004745422355337548603790605318968572772447260620450953389789527829160036210821800758630313480533176033727919668746581046562929869336432778215183512002299107442967887221305090225490360272535738417728939435264785219583L)
        self.assertEqual (unum.negbigu, 277600968361828440402775265597020434815997013204988587085620093640803064110231859701556417882431901762362254332654716007948827941730592096896640241473719459196916882360688716004581829478912654111013133797181128986406139309714666728957178196861435813292938198064699970327764031717773841377906465705687240113594587906444532709966742881253758812345453032590690987854815175860540949471604461423578493372589239372579004745422355337548603790605318968572772447260620450953389789527829160036210821800758630313480533176033727919668746581046562929869336432778215183512002299107442967887221305090225490360272535738417728939435264785154047L)
        self.assertEqual (unum.qNaNu, 138800484180914220201387632798510217407998506602494293542810046820401532055115929850778208941215950881181127166327358003974413970865296048448320120736859729598458441180344358002290914739456327055506566898590564493203069654857333364478589098430717906646469099032349985163882015858886920688953232852843620056797293953222266354983371440626879406172726516295345493927407587930270474735802230711789246686294619686289502372711177668774301895302659484286386223630310225476694894763914580018105410900379315156740266588016863959834373290523281464934668216389107591756001149553721483943610652545112745180136267869208864469717632392626175L)
        self.assertEqual (unum.sNaNu, 277600968361828440402775265597020434815997013204988587085620093640803064110231859701556417882431901762362254332654716007948827941730592096896640241473719459196916882360688716004581829478912654111013133797181128986406139309714666728957178196861435813292938198064699970327764031717773841377906465705687240113594587906444532709966742881253758812345453032590690987854815175860540949471604461423578493372589239372579004745422355337548603790605318968572772447260620450953389789527829160036210821800758630313480533176033727919668746581046562929869336432778215183512002299107442967887221305090225490360272535738417728939435264785252351L)
        self.assertEqual (unum.negopeninfu, 491520)
        self.assertEqual (unum.posopeninfu, 229376)
        self.assertEqual (unum.negopenzerou, 294912)
        self.assertEqual (unum.maxreal, 2830922062089909578003106055489903202696261422944776334468771496544733268481690507192050712953296830150951745923312252984779617159089475697763876592501746383487855587089826022100325302555914059693920423566485867042415090826969939713703702282577030326402965990778110194921244197271350006707858448557165871328832525145546616306555028692960626743977225258962967124876357857917735555700144396632349682503911181993344037290187281701607359260440734402767689733582898569475036525626246166878074487356880841794279847556557905540624637556658009789094130978155193670792034307206340100742604029524887745402222759108968619437324526169027088190201464842085247031995319174908954312117658286027766815245690789410620119466939680719359957090950827465158134012372613470344123133143084691847648865013146997142042597304458203485057393621169605736086371774875533153610440985180759282923958818749626681492329801079274265422098922477554560247252051203132815521802856177251519441932600958224759704264235358865736771769218607116890169845678009426247722633545263275369153304373604523068393411379065200468936408410965037676520911507054737354546438910364340111845032635208444303707153815488292218508487179354107653412808718309572515836468005253901819868523928227756461191754063394788230437138819656186724500420428544756772788255969581178259177733185854473093795000928181039933946100928912098664748950825069826302669887124980295880539285545843880261894977106100195753775408498665179288555347055814803633738343149526773872383593934617479135743041963824780916239044775847221898024686877379751664337713328988758494276959741514291968767563003608621000420899606272851455198973576118813140667157415115026106229628458397717419138601685702299088919996296864784122325181180122967964603758383135965531586693260830693649721277867007726313610624029985000558909425599156830593492908934145220663881378741123492002543842722198219104238018515663528632367508558909175899777436174609596136475213870599376714526837312604174133189756362689893542131027187452000039246434370447298718479785959671088654239965045814107207755747986543900888933063734261910488594788715489803754712629415263371723288784980111268709959864983282362955650014760256862766703839165211989324090728863167350573523498591233925519356554626071031453127397423210871193469933473425737966266653333786100203184149852009299235479236684638922385590971704401823314095890884970352109013480116369530756880705984509845076476209948614706293435850774547073635061934518392670378899461348665669852422408737489508941455667286531101272630056310235787588665131671507202316523599080724928064510902550504073056751454532376990962206458903295475560802078948396067653600114164298484398771802441806436185219041482962048125364823095189968863553897547193294654379235949781213070248425788075159371335334310233481343535813530119953892809414165356207234890738854030207714928835407655511790588593953725253760657805810030930929471440016218434340646560505309404270618191547253415620885841098636083566726536358235984914897262041793795064576551701104425708124005944195338323367280667458238677069808476841382377170218744104971409984994005356342149919268858965413067984809444183321359099667319501066006724409829407808524278565367729672615490715794186375130893851837735339344118626358616901307836268448713362659073581761157673210879767697713617576364862715884553449365055231769494129650083502927373133334862123172527752131294461530904551094991840396600224558980951741637683090532417978408897212302976504476441846394169246605873676523007914426592647772888333705228837850373682630847202145158518655628608830446423618218314942665227131548584354166986923489773482210297611326996073974089247556075534664601495937106308173186065792864243531513583051977960796010204945978857305539216138067795800251765506326355208402874418826375380676806694792066574641319335247785599289894027607437651426432154478040462021962444770002479999079607493143036912984293741242724047285964074674299240926185081385712081809766681860618747196867968906623499479364446819197022834349890799862909135502170013487755318664547609290258738849764874816579090577072746726468178430189356510277107812444569895659103808657376553943037184790212806679950781341820437619595841028809444519916906474232406641687532677223455792826115784411761728252282995380222946565951017849600999330023766914647611880833515092768887261397379424017658876007635023277256932832951803057992048452991645756358477943487428312253023509854365175769728094130235825418990672216262400181234741351572567491184530987308408634072127276456235324868971584585043555710921621559030115678295825854858719114292295465311478180022325188822809518605029196459956426804937423894617708339645834434331145333711924330786657565726630004872588028067094948749402259532385898300100428479642668357821143349965393247359546740909769274398121320129124721024604059175445175754843164788840616719692044948840883950781114716779301988963384506494051251890538893663964112863019957275614706425941682203991877049077082395404658956011024785609005551108013195498108400537996524987623081005216356446021904372683600503481105665762521783462682370265349290785040490202123095207652088481796062852409870753750047757434956002847944675938085925036847793015761090106118246328194734868964967179684227803511334125005763619050537362047280293057236939470098273476134689600738691151716400583570807809199140009543399655097012752975895464564663929004427330000128493269618378851789520904131684962740464221391530487771986112793426717712384557911221504979679988701144398141189400893606524008639972453875668950209526820089545112713983794421116981347942813480262687587696916955221623120922075226103821747537964779736878100431229618501673042380912716736079313233536100989892352856980914201773297720542901298858095166066102418070875215510780444661953196236075718867134508799715173381299613334302830939847980419344205549253881784926040276662240383447740405624131975984493027533960348452473596665079095439971997679094326588780108126044177027822593789751986762222056737176157048852569684290026661454386342117270499845646312656622868254284006730064105442518679832701476065432393406166898629359353848086056385336397112344390930461755954175140732182913969116261728245959833047433985475871165241945558456674954000059231276348307257368946037681525182995836742342367431325818132116450991029164004016034188308941006289936177551281969109450430759658305297038118833426389951520671887814284717801177894466462702736670907986906314863200420149009026771559099207746561661047381925758814834049831031378697786538999500569799997752610245339274680301595377856290871320535874495420739689198805096288686872243196938327803856833318273531774910480848220299842681300523646590716773399397815777447437467309726084981290731370437849815446096386391988858387948280339526340617970195361453475784759093560194317767175189157600589469315272596603714982739853990650111770797558402483943966458148966534302152834753127313209156592068854370954600375430900295526942521777637154587677066691732146372585573824403404762283901249350731107463372137453267892067960577963600580766445099854996150991062663263361735415542827641524463442967129062419445133108592273818020009450127453586956447471033558292638277053081519817283848721872373710234771437271814102582981783647451776144579559377570216493752929849289220867896961772592172699447625814120369290283609066277008553670841025252549762379526854302425583985733306293114693916559711565258906236900454539020908150169734450429460165718597657869859191415592118910944295386770795270542004645970740789231396576720955456148100576447485641101517155935144591878349028340395780161327540103494698584220180382348343638561224133917869588263251603869124738379141524323450624027853155801627436799614777652695237260986821031456876291628521052424959288267753411850940130521644720427853768654071763698423469963201321799508712460267925983656183365960396179935986758182622478262350569362644002146528899095179680631421205593863921030687544592941487995293316870324237505308869423385339443865885636745761302644315521455616318462730032019471973696181249769597623037717151605162854386808650997132695539606975602087351624827818736158745472296128194631310634793476864426041357214617707893187044108459692145330538071168692469843705028881251331339522173441277764462226769853614674164881583455241692957694520845700112980978130909667429561446551866505672272521903635245396294654796477186128237074423826354024802669761468048603325897994568825044842411144032344828805182376076719177259710631412860827413256029686197643624597478893223075558665549185090795252571888200919572266377203266704081179707706890506978479096324251848310574254857344580682126418866640965463761529766105335026278227461598508857314758905594299582156559793310927073395774935895251477146544404622559730624916376811222285519158468103239926604018747570581221193904400500085399878797420368776951226867779927191027278061380939998844047210939339961136632362579486960252414976414580075167715034358972114730016782287767223220860986030012162927258997764902284789232551104771749105387437349945308584393847001609248503769744990461294329619939710007082991906384698891315765907724705342374254412577108805653916465270305708718385382503386669252344704326933274830366404912089514666210412255217763678827360338202499299042247892182543964661175019390887835348296657066673570514885529336173619039705181436658524702252480765644634781340528357302200185477466720445460006226087864871832059891988308131847147403629338999154920664943167137613990596696904961960880756316590972695599704076526361287840472729032316262020481078115576920120305835084439102852047384080279452486013293767898045979790021773273873318773705469363201644359946899074956065332629619366236100522420401560002903924854284154890942294814643977278969067637648315825368472932746308999839267850395645990158835873651673236299419197440062914560L)
        self.assertEqual (unum.smallsubnormal, 0.0)

suite = unittest.TestLoader().loadTestsFromTestCase(TestSetenv)

if __name__ == '__main__':
    unittest.main()
