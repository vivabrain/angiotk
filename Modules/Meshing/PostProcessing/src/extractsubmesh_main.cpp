
#include <feel/feelcore/environment.hpp>

#include <postprocessing.hpp>


int main( int argc, char** argv )
{
    using namespace Feel;

    po::options_description myoptions = ExtractSubMeshFromFSIMesh<>::options( "" );

    Environment env( _argc=argc, _argv=argv,
                     _desc=myoptions,
		     _about=about(_name="extractsubmesh",
				  _author="Feel++ Consortium",
				  _email="feelpp-devel@feelpp.org"));

    ExtractSubMeshFromFSIMesh< Mesh<Simplex<3> > > myExtract( "");
    myExtract.run();

    return 0;
}
