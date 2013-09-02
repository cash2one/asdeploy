/*
 * Ext JS Library 2.0.1
 * Copyright(c) 2006-2008, Ext JS, LLC.
 * licensing@extjs.com
 *
 * http://extjs.com/license
 */
Ext.onReady(function(){
	//LoadLangFile.loadFile('js/lang/Lang-mysky');
	//LoadLangFile.loadFile('js/lang/Lang-flow');
	
    UpdatePageInfo('advancedSearchTitle', '高 级 搜 索');
    Navigation.init([{
        name: '高 级 搜 索'
    }]);
    Ext.QuickTips.init();
    
    var UserField = [{
        name: 'id'
    }, {
        name: 'name'
    }, {
        name: 'englishName'
    }];
    
    var categoryDs = new Ext.data.Store({
        url: 'topic.do?action=getFirstLevelTopics',
        autoLoad: true,
        listeners: {
            load: function(){
                //	categoryCombox.setValue(categoryCombox.store.collect('id', true)[0]); // FINAL LINE
            }
        },
        reader: new Ext.data.JsonReader({
            root: 'result.list', // root of data... comment it if necessary
            id: 'id'
        }, UserField)
    });
    
    var comboCategories = new Ext.form.ComboBox({
        store: categoryDs,
        //forceSelection:true,	
        id: 'categoryCombo',
        mode: 'local',// very important
        displayField: "name",
        valueField: "id",
		editable: false,
        emptyText: '全部分类',
        selectOnFocus: true,
        triggerAction: 'all',
        width: 210
    });
    var dataSer = [['服  务', 'service'], ['用  户', 'member']];
    
    var dataService = new Ext.data.Store({
        reader: new Ext.data.ArrayReader({}, [{
            name: 'serviceList'
        }, {
            name: 'service'
        } // {name: 'lastChange', type: 'date', dateFormat: 'n/j h:ia'}
		])
    });
    dataService.loadData(dataSer);
    var comboService = new Ext.form.ComboBox({
        store: dataService,
        id: 'advancedSearchType',
        name: 'advancedSearchType',
        mode: 'local',// very important
        displayField: "serviceList",
        valueField: "service",
        blankText: '服  务',
        emptyText: '服  务',
		editable: false,
        selectOnFocus: true,
        triggerAction: 'all',
        width: 110,
        listeners: {
            select: function(combox, record, index){
                var type = record.data.service;
                if (type == 'member') {
					document.getElementById('serviceList').style.display = 'none';
					document.getElementById('serviceSearchFields').style.display = 'none';
					document.getElementById('memberList').style.display = 'block';
					document.getElementById('memberSearchFields').style.display = 'block';
				} else {
					if (type == 'service') {
						document.getElementById('serviceList').style.display = 'block';
						document.getElementById('serviceSearchFields').style.display = 'block';
						document.getElementById('memberList').style.display = 'none';
						document.getElementById('memberSearchFields').style.display = 'none';
					}
				}
            }
        }
    });
	
	var countryBoxDS = new Ext.data.SimpleStore({
        fields: ['id', 'name'],
        data: InsertArray(['全部国家', '全部国家'], LocalData.country, 0)
    });
    comboLocation = new Ext.form.ComboBox({
        id: 'locationStr',
        store: countryBoxDS,
        displayField: LoadLangFile.isZh() ? 'name' : 'id',
        forceSelection: 'true',
        valueField: 'id',
        typeAhead: false,
        mode: 'local',
        triggerAction: 'all',
        emptyText: '选择国家',
        selectOnFocus: true,
        resizable: false,
        editable: false,
        width: 150,
        listWidth: 150
    });
	
    var doSearch = function(){
		var searchType = (comboService.getValue() == '' ? 'service' : comboService.getValue());
        var searchFields = "";
        var artifactTypes = "";
		var accountTypes = "";
        if (searchType == 'service') {
			if (document.getElementById("searchTitle").checked) 
				searchFields = "_name,";
			if (document.getElementById("searchDescription").checked) 
				searchFields = searchFields + "_description,";
			if (document.getElementById("searchTag").checked) 
				searchFields = searchFields + "_tags";
			if (document.getElementById("searchLivesession").checked) 
				artifactTypes = "Livesession,";
			if (document.getElementById("searchReference").checked) 
				artifactTypes = artifactTypes + "Course,";
			if (document.getElementById("searchMostwanted").checked) 
				artifactTypes = artifactTypes + "Mostwanted";
		} else if (searchType == "member"){
			if (document.getElementById("searchUserName").checked) 
				searchFields = searchFields + "_user,"
			if (document.getElementById("searchScreenName").checked) 
				searchFields = searchFields + "_name,"
			if (document.getElementById("searchMemberDescription").checked) 
				searchFields = searchFields + "_description,";
			if (document.getElementById("searchMemberTag").checked) 
				searchFields = searchFields + "_tags";
			if (document.getElementById("searchIndividual").checked&&document.getElementById("searchBestOfWorld").checked) {
				artifactTypes = "Account,";
			} else if (document.getElementById("searchBestOfWorld").checked) {
				artifactTypes = "Account,";
				accountTypes = "bestUser";	
			} else if(document.getElementById("searchIndividual").checked) {
				artifactTypes = "Account,";
				accountTypes = "normalUser";	
			}
			if (document.getElementById("searchOrganization").checked) { 
				artifactTypes = artifactTypes + "Organization,";
			}
		}
        var searchParams = {
            s: document.getElementById("searchkeyword").value,
            category: Ext.getCmp("categoryCombo").getValue() == '全部分类' ? 'all' : Ext.getCmp("categoryCombo").getValue(),
			searchType: 'service',
            searchFields: searchFields,
            artifactTypes: artifactTypes,
            accountTypes: accountTypes,
			locationStr: comboLocation.getValue()
        };
        location.href = 'search.do?s=' + searchParams.s +
        '&category=' +
        searchParams.category +
        '&searchType=' +
        searchParams.searchType +
        '&searchFields=' +
        searchParams.searchFields +
        '&artifactTypes=' +
        searchParams.artifactTypes +
        '&accountTypes=' +
		searchParams.accountTypes +
		'&locationStr=' +
        searchParams.locationStr +
        '&fun=doAdvancedSearch';
    };
    
    var advSearchBtn = new Ext.Button({
             id:"searchButton",
             name:"search",
             style:"color:#ffffff;", 
             text:"<font style=\"color:#ffffff;\" >" + '搜        索' + "</font>",
             handler:doSearch
             });
	
    
    var p = new Ext.Panel({
        header: false,
        collapsible: false,
        renderTo: 'advancedSearch',
        width: static_data.ab_panelWidth,
        cls: '',
        buttonAlign: 'center',
        border: false,
        items: [{
            layout: 'column',
            items: [{
                columnWidth: .08,
                xtype: 'panel',
                baseCls: '',
                html: '<div class="fontbold">' + '搜        索' + ':</div>'
            }, {
                columnWidth: .47,
                xtype: 'panel',
                baseCls: '',
                html: '<input id="searchkeyword" maxlength="50" type="text" size=58>'
            }, {
                columnWidth: .28,
                height: 28,
                items: [comboCategories]
            }, {
                columnWidth: .17,
                height: 30,
                items: [comboService]
            }]
        }, {
			id: 'serviceSearchFields',
            layout: 'column',
            style: 'margin-top:20px;margin-left:70px',
            items: [{
                width: 25,
                height: 17,
                html: '<input id="searchTitle" name="" type="checkbox" value=""> '
            }, {
                width: 110,
                height: 17,
                style: Ext.isIE?'margin-top:4px': '',
                html: '<div style="vertical-align:middle">' +  '搜索标题' + '</div>'
            }, {
                width: 25,
                height: 17,
                html: '<input id="searchTag" name="" type="checkbox" value=""> '
            }, {
                width: 110,
                style: Ext.isIE?'margin-top:4px': '',
                html: '<div style="vertical-align:middle">' + '搜索标签' + '</div>'
            }, {
                width: 25,
                height: 17,
                html: '<input id="searchDescription" name="" type="checkbox" value=""> '
            }, {
                width: 150,
                style: Ext.isIE?'margin-top:4px': '',
                html: '<div style="vertical-align:middle">' + '搜索说明' + '</div>'
            }]
        }, {
			id: 'memberSearchFields',
            layout: 'column',
            style: 'margin-top:20px;margin-left:70px;display:none',
            items: [{
                width: 25,
                height: 17,
                html: '<input id="searchUserName" name="" type="checkbox" value=""> '
            }, {
                width: 125,
                height: 17,
                style: 'vertical-align:middle',
                html: '<div style="vertical-align:middle">' + '搜素用户名' + '</div>'
            }, {
                width: 25,
                height: 17,
                html: '<input id="searchScreenName" name="" type="checkbox" value=""> '
            }, {
                width: 135,
                height: 17,
                style: 'vertical-align:middle',
                html: '<div style="vertical-align:middle">' + '搜素显示名' + '</div>'
            }, {
                width: 25,
                height: 17,
                html: '<input id="searchMemberTag" name="" type="checkbox" value=""> '
            }, {
                width: 85,
                style: '',
                html: '<div style="vertical-align:middle">' + '搜索标签' + '</div>'
            }, {
                width: 25,
                height: 17,
                html: '<input id="searchMemberDescription" name="" type="checkbox" value=""> '
            }, {
                width: 150,
                style: 'vertical-align:middle',
                html: '<div style="vertical-align:middle">' + '搜索说明' + '</div>'
            }]
        }, {
            xtype: 'panel',
            baseCls: '',
            html: '<div class="abDotRepeatTop"></div>'
        }, {
            xtype: 'panel',
            baseCls: '',
            cls: ' ',
            html: '<div class="ablableSNew">' + '按服务类型搜索' + '</div>'
        }, {
            layout: 'column',
            id: 'serviceList',
            style: 'margin-top:15px;height:31px',
            items: [{
                width: 25,
                style: 'margin-top:5px',
                html: '<span  class="forInput"><input id="searchLivesession" name="" type="checkbox" value=""/></span> '
            }, {
                width: 120,
                html: '<span class="golive"  style="line-height:2em;verticle-align:middle">' + '远 程 面 授' + '</span>'
            }, {
                width: 25,
                style: 'margin-top:5px',
                html: '<input id="searchReference" name="" type="checkbox" value=""> '
            }, {
                width: 120,
                html: '<span class="course"  style="line-height:2em;verticle-align:middle">' + '专 业 资 料' + '</span>'
            }, {
                width: 25,
                style: 'margin-top:5px',
                html: '<input id="searchMostwanted" name="" type="checkbox" value=""> '
            }, {
                width: 120,
                html: '<span class="mostwanted"  style="line-height:2em;verticle-align:middle">' + '需 求 悬 赏' + '</span>'
            }]
        }, {
            layout: 'column',
            id: 'memberList',
            style: 'margin-top:15px;display:none',
            items: [{
                width: 25,
                html: '<input id="searchIndividual" name="" type="checkbox" value=""> '
            }, {
                width: 120,
                html: '<span class="myprofileBtn iconP">' + '用户' + '</span>'
            }, {
                width: 25,
                html: '<input id="searchOrganization" name="" type="checkbox" value=""> '
            }, {
                width: 120,
                html: '<span class="orgnizationIcon iconP">' + '机构' + '</span>'
            }, {
                width: 25,
                html: '<input id="searchBestOfWorld" name="" type="checkbox" value=""> '
            }, {
                width: 120,
                html: '<span class="bestIcon iconP">' + '权威人士' + '</span>'
            }]
        }, {
            xtype: 'panel',
            baseCls: '',
            html: '<div class="ablableSNew ">' + '国家' + '</div>'
        }, {
            cls: '',
             height: 30,
            items: [comboLocation]
        }, {
            xtype: 'panel',
            baseCls: '',
            
            html: '<div class="abDotRepeatTop"></div>'
        }],
        
        buttons: [advSearchBtn]
    });
});
