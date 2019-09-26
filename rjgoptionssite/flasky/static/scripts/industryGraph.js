    class Industry{
            constructor(data){
                this.name = data["name"];
                this.id = data["id"];
                this.desc = data["desc"]

                this.relations = [];
                this.knowies = [];
                this.friends = [];
            }

            setView(view){
                this.view = view;
            }

            getView(){
                return this.view;
            }

            addRelation(relation){
                this.relations.push(relation);
            }

            addRelated(related,type){
                if (type == 1)
                    this.knowies.push(related);
                if (type == 2)
                    this.friends.push(related);
            }

            toString(){
                return this.id + " " + this.name;
            }
        }

        class IndustryCircle{
            constructor(industry,x,y,r,c){
                this.industry = industry;
                this.x = x;
                this.y = y;
                this.r = r;
                this.c = c;
                this.industry.setView(this);
            }

            registerSvg(svg){
                this.svg = svg;
            }


            showUp(role){
                let colors = ["","blue","green"];
                d3.select(this.svg)
                    .transition()
                    .attr("r",this.r * 1.25)
                    .style("fill", colors[role]);
            }
            showOff(role){
                d3.select(this.svg)
                    .transition()
                    .attr("r",this.r)
                    .style("fill", this.c);
            }


            mouseOver(){
                d3.select(this.svg)
                    .transition()
                    .attr("r",this.r * 1.5)
                    .style("fill", "orange");

                d3.select("#rightbar")
                    .html(this.industry.desc)

                for(var rel in this.industry.relations){
                    let relation = this.industry.relations[rel];
                    let relationLine = relation.getView();
                    relationLine.showUp();
                }

                for (var related in this.industry.friends){
                    let relatedIndustry = this.industry.friends[related];
                    let relatedIndustryCircle = relatedIndustry.getView();
                    relatedIndustryCircle.showUp(2);
                }
                for (var related in this.industry.knowies){
                    let relatedIndustry = this.industry.knowies[related];
                    let relatedIndustryCircle = relatedIndustry.getView();
                    relatedIndustryCircle.showUp(1);
                }
            }

            mouseOut(){
                this.showOff();

                d3.select("#rightbar")
                    .html("")

                 for(var rel in this.industry.relations){
                    let relation = this.industry.relations[rel];
                    let relationLine = relation.getView();
                    relationLine.showOff();
                }
                for (var related in this.industry.friends){
                    let relatedIndustry = this.industry.friends[related];
                    let relatedIndustryCircle = relatedIndustry.getView();
                    relatedIndustryCircle.showOff();
                }
                for (var related in this.industry.knowies){
                    let relatedIndustry = this.industry.knowies[related];
                    let relatedIndustryCircle = relatedIndustry.getView();
                    relatedIndustryCircle.showOff();
                }
            }

            toString(){
                return this.industry + "@" + this.x + ":" + this.y;
            }
        }

        class Relation{
            constructor(data){
                this.id = data["id"];
                this.between = [];
                this.type = data["type"];
            }

            setView(view){
                this.view = view;
            }

            getView(){
                return this.view;
            }

            addIndustry(industry){
                this.between.push(industry);
            }

            toString(){
                return this.id + ":" + this.between[0] + " vs " + this.between[1];
            }
        }

        class RelationLine{
            constructor(relation,x1,y1,x2,y2,w){
                this.relation = relation;
                this.x1 = x1;
                this.y1 = y1;
                this.x2 = x2;
                this.y2 = y2;
                this.w  = w;
                this.color = ["","lightblue","lightgreen"][this.relation.type];
                this.relation.setView(this);
            }

            registerSvg(svg){
                this.svg = svg;
            }

            showUp(){
                let colors = ["","blue","green"];
                d3.select(this.svg)
                    .style("stroke",colors[this.relation.type])
                    .style("stroke-width",this.w * 2);
            }

            showOff(){
                d3.select(this.svg)
                    .style("stroke",this.color)
                    .style("stroke-width",this.w);
            }

            toString(){
                return this.x1 + ":" + this.y1 + " to " + this.x2 + ":" + this.y2;
            }
        }

        class Builder{
            constructor(industryData,relationData){
                let industriesMap = {}
                this.industries = [];
                this.relations = [];

                for(var i = 0 ; i < industryData.length;i++){
                    let industry = new Industry(industryData[i]);
                    industriesMap[industryData[i]["id"]] = industry;
                    this.industries.push(industry);
                }

                for(var r = 0 ; r < relationData.length;r++){
                    let data = relationData[r];

                    let relation = new Relation(data);
                    let industry1 = industriesMap[data["between"][0]];
                    let industry2 = industriesMap[data["between"][1]];

                    relation.addIndustry(industry1);
                    industry1.addRelation(relation);

                    relation.addIndustry(industry2);
                    industry2.addRelation(relation);

                    industry1.addRelated(industry2,relation.type);
                    industry2.addRelated(industry1,relation.type);

                    this.relations.push(relation);
                }

            }
        }

        class SceneBuilder{
            constructor(industries,relations){
                let industryCircleRadius = 20;
                let neutralColor = "gray";

                let industryCount = industries.length;
                var graphRadius = industryCount * industryCircleRadius * 3  / (2 * Math.PI);
                if (graphRadius < 250){
                    graphRadius = 250;
                }

                this.sceneWidth = graphRadius * 6;
                this.sceneHeight = graphRadius * 3;

                this.xCenter = this.sceneWidth / 2;
                this.yCenter = this.sceneHeight / 2;

                this.industryCircles = [];
                for(var i = 0; i < industries.length; i++){

                    let x = graphRadius * Math.cos(Math.PI * 2 * ((i + 0.1)/industryCount));
                    let y = graphRadius * Math.sin(Math.PI * 2 * ((i + 0.1)/industryCount));

                    let industryCircle = new IndustryCircle(industries[i],x + this.xCenter,y + this.yCenter,industryCircleRadius,neutralColor);
                    this.industryCircles.push(industryCircle);
                }

                this.relationLines = [];
                for(var r = 0; r < relations.length; r++){
                    let rel = relations[r];

                    let side1 = rel.between[0].getView();
                    let side2 = rel.between[1].getView();

                    let relationLine = new RelationLine(relations[r],side1.x,side1.y,side2.x,side2.y,3);
                    this.relationLines.push(relationLine);
                }
            }

        }